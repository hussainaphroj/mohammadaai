import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="MohammadAAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"
MODELS = [
    DEFAULT_MODEL,
    "openai/gpt-oss-20b:free",
    "meta-llama/llama-3.3-70b-instruct:free",
]

st.markdown("""
<style>
    :root { color-scheme: dark; }
    .stApp {
        background: radial-gradient(ellipse at top left, #101d39 0%, #080e1a 45%, #070b13 100%);
        color: #eef4ff;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0e1728 0%, #080f1d 100%);
        border-right: 1px solid #243651;
    }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1450px; }
    .hero {
        padding: 1.4rem 1.6rem; border: 1px solid #253a5a; border-radius: 22px;
        background: linear-gradient(120deg, rgba(22,42,75,.96), rgba(10,19,34,.96));
        margin-bottom: 1.3rem; box-shadow: 0 14px 45px rgba(0,0,0,.18);
    }
    .brand { font-size: clamp(2rem, 4vw, 3.25rem); font-weight: 850; letter-spacing: -1.5px; line-height: 1.1; }
    .brand span { color: #35b9ff; }
    .subtitle { color: #b9c9e8; font-size: 1.1rem; margin-top: .45rem; }
    .muted { color: #9aafd1; }
    .panel {
        padding: 1.15rem 1.25rem; border-radius: 16px; border: 1px solid #263954;
        background: rgba(15,25,43,.82); margin-bottom: .9rem;
    }
    .chat-user {
        background: linear-gradient(120deg, #123768, #102642); border: 1px solid #2266a5;
        padding: 1rem 1.15rem; border-radius: 16px 16px 4px 16px; margin: .5rem 0 1rem auto;
        max-width: 92%; overflow-wrap: anywhere;
    }
    .chat-assistant {
        background: linear-gradient(120deg, rgba(20,32,52,.98), rgba(13,23,39,.98));
        border: 1px solid #2a3e5c; padding: 1.1rem 1.2rem; border-radius: 4px 16px 16px 16px;
        margin: .5rem 0 1.1rem; overflow-wrap: anywhere;
    }
    .chat-label { font-weight: 750; color: #39c4ff; margin-bottom: .4rem; }
    div.stButton > button {
        border-radius: 12px; border: 1px solid #287edb; font-weight: 700;
        min-height: 2.8rem;
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(100deg, #0879f9, #2458ed); color: white;
    }
    .stTextArea textarea, .stTextInput input {
        background: #0c1627 !important; border: 1px solid #2d4668 !important; border-radius: 12px !important;
    }
    [data-testid="stChatInput"] textarea { background: #0c1627 !important; }
    hr { border-color: #263954; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

def get_api_key():
    key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not key:
        #key = st.session_state.get("session_api_key", "").strip()
        key = st.secrets.get("OPENROUTER_API_KEY", "")
    return key

def ask_openrouter(messages, model, reasoning):
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is missing. Add it to your .env file or enter it in the sidebar.")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Title": "MohammadAAI",
    }
    payload = {
        "model": model,
        "messages": messages,
        "reasoning": {"enabled": reasoning},
    }
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=120,
    )
    if not response.ok:
        try:
            detail = response.json().get("error", {}).get("message", response.text)
        except ValueError:
            detail = response.text
        raise RuntimeError(f"OpenRouter returned HTTP {response.status_code}: {detail}")
    data = response.json()
    choices = data.get("choices", [])
    if not choices:
        raise RuntimeError(f"No answer was returned by the model: {data}")
    message = choices[0].get("message", {})
    content = message.get("content") or ""
    if not content.strip():
        content = "The model returned no text content. Try disabling reasoning or selecting another model."
    return content, message

if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_api_key" not in st.session_state:
    st.session_state.session_api_key = ""

with st.sidebar:
    st.markdown("## 👋 Hello!")
    st.markdown("I'm **MohammadAAI**, your AI assistant. Ask me anything!")
    st.divider()
    st.markdown("### 🧠 Model settings")
    model = st.selectbox("Choose a model", MODELS, index=0)
    reasoning = st.toggle("Enable reasoning", value=True, help="Requests reasoning support from models that support it.")
    st.caption("Reasoning availability and returned content depend on the selected model.")
    st.divider()
    st.markdown("### 🔐 API key")
    if os.getenv("OPENROUTER_API_KEY", "").strip():
        st.success("API key loaded from .env")
    else:
        st.session_state.session_api_key = st.text_input(
            "OpenRouter API key",
            value=st.session_state.session_api_key,
            type="password",
            placeholder="sk-or-v1-…",
            help="Used for this session only. Prefer a local .env file for regular use.",
        )
        st.caption("Never share your API key or commit it to Git.")
    st.divider()
    st.markdown("### 💡 Quick tips")
    st.markdown("- Ask about coding, DevOps, Linux, cloud, or AI.\n- Include error messages for troubleshooting.\n- Type a follow-up to continue the conversation.")
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("Powered by OpenRouter · Built with Streamlit")

left, right = st.columns([5, 1.4], vertical_alignment="center")
with left:
    st.markdown("""
    <div class="hero">
      <div class="brand">🤖 Mohammad<span>AAI</span></div>
      <div class="subtitle">Your intelligent AI assistant 🚀</div>
      <div class="muted">Ask a question, explore an idea, or solve a problem.</div>
    </div>
    """, unsafe_allow_html=True)
with right:
    st.markdown("""
    <div class="panel" style="text-align:center">
      <div style="font-size:1.8rem">⚡</div>
      <b>Powered by</b><br><span style="color:#39baff;font-weight:800">OpenRouter</span><br>
      <span style="color:#42df9a">● Ready</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### 💬 Chat with MohammadAAI")
if not st.session_state.messages:
    st.markdown("""
    <div class="panel">
      <h3 style="margin-top:0">Start a conversation</h3>
      <p class="muted">Type your question below and get an answer from MohammadAAI.</p>
      <p>✨ Try asking:</p>
      <ul>
        <li>Explain Terraform with a simple example</li>
        <li>Help me troubleshoot a Linux issue</li>
        <li>Write a Python script to automate a task</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

for item in st.session_state.messages:
    if item["role"] == "user":
        st.markdown(
            f'<div class="chat-user"><div class="chat-label" style="color:#8dd7ff">You</div>{item["content"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="chat-assistant"><div class="chat-label">🤖 MohammadAAI</div>', unsafe_allow_html=True)
        st.markdown(item["content"])
        st.markdown("</div>", unsafe_allow_html=True)

prompt = st.chat_input("Type your question here…")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("MohammadAAI is thinking…"):
        try:
            answer, raw_message = ask_openrouter(
                st.session_state.messages,
                model,
                reasoning,
            )
            st.session_state.messages.append({"role": "assistant", "content": answer})
            # Keep a returned reasoning summary only if the provider includes one.
            reasoning_details = raw_message.get("reasoning")
            if reasoning_details:
                st.session_state.last_reasoning = reasoning_details
        except Exception as exc:
            st.error(str(exc))
    st.rerun()

if st.session_state.get("last_reasoning") and reasoning:
    with st.expander("🧩 Reasoning summary (if provided by the model)"):
        st.write(st.session_state.last_reasoning)

st.markdown("""
<div style="text-align:center;color:#8ea4c8;padding:1rem 0 .3rem">
  <b>MohammadAAI</b> &nbsp;•&nbsp; Built with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
