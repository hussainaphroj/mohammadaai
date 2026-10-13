# MohammadAAI

A Streamlit chat UI powered by OpenRouter.

## 1. Set up Python

Python 3.10 or newer is recommended.

### Windows (PowerShell)

```powershell
cd MohammadAAI
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Edit `.env` and replace the placeholder with your OpenRouter API key.

### Linux / macOS

```bash
cd MohammadAAI
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
nano .env
```

Add your API key to `.env`:

```dotenv
OPENROUTER_API_KEY=sk-or-v1-your_actual_api_key
```

## 2. Run the app

```bash
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`. Open it in your browser.

## Features

- MohammadAAI dark theme and responsive Streamlit layout
- OpenRouter model selector
- Reasoning toggle for compatible models
- Multi-turn chat history during the current session
- Clear conversation control
- API error messages for troubleshooting
- API key loaded from `.env` (never hardcode the key in `app.py`)

## Security

- Never commit `.env` or share your API key.
- `.env.example` is only a placeholder template.
- A session-entered key is kept in Streamlit session state for that session.
- Model names and free-tier availability can change; check your OpenRouter account if a model returns an access error.
