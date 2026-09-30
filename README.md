# Document question answering + Browser Agents

A Streamlit app that answers questions about uploaded documents via OpenAI, extended with **browser-use** autonomous browser agents and **CUA** (Computer-Use Agent) demos.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://document-question-answering-template.streamlit.app/)

## Quick start

1. Install the requirements and Playwright browser:

   ```bash
   pip install -r requirements.txt
   python -m playwright install chromium
   python -m playwright install-deps chromium
   ```

2. Copy `.env.example` to `.env` and add your API keys:

   ```bash
   cp .env.example .env
   ```

3. Run the Streamlit app:

   ```bash
   streamlit run streamlit_app.py
   ```

## Demo scripts

| Script | What it does | Key required |
|--------|-------------|--------------|
| `scripts/browser_agent_demo.py` | Browser-Use agent navigates Hacker News | `OPENAI_API_KEY` (or runs Playwright smoke test without) |
| `scripts/cua_demo.py` | CUA loop — model sees screenshots, emits browser actions | `OPENAI_API_KEY` |
| `scripts/agents_sdk_cua_demo.py` | OpenAI Agents SDK `ComputerTool` (separate venv) | `OPENAI_API_KEY` |

```bash
python scripts/browser_agent_demo.py
python scripts/cua_demo.py
```

## OpenAI Agents SDK (separate venv)

`browser-use` pins `openai==2.26` while `openai-agents` requires `openai>=3.0`. Install the Agents SDK in a separate virtualenv:

```bash
python -m venv .venv-agents && source .venv-agents/bin/activate
pip install -r requirements-openai-agents.txt
python -m playwright install chromium
python scripts/agents_sdk_cua_demo.py
```
