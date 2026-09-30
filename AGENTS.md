## Cursor Cloud specific instructions

This repository is a Streamlit document Q&A app extended with **browser agent** and **computer-use agent (CUA)** capabilities.

### Architecture overview

| Component | File(s) | Purpose |
|-----------|---------|---------|
| Streamlit app | `streamlit_app.py` | Document Q&A via OpenAI GPT models |
| Browser-Use agent demo | `scripts/browser_agent_demo.py` | Autonomous browser agent (headless Chromium) |
| CUA demo (openai 2.x) | `scripts/cua_demo.py` | Computer-use-preview model controlling Playwright |
| Agents SDK CUA demo | `scripts/agents_sdk_cua_demo.py` | OpenAI Agents SDK `ComputerTool` (separate venv) |
| MCP setup | `scripts/setup-mcp.sh`, `.cursor/mcp.json` | Hugging Face MCP server for agent tooling |

### Dependencies

**Primary virtualenv** (`requirements.txt`):

- `streamlit>=1.64.0` — web UI framework
- `browser-use>=0.13.10` — browser agent framework (brings `openai==2.26.0`, `playwright`, `langchain`, Anthropic/Google/Groq clients)
- `playwright>=1.63.0` — headless browser automation
- `python-dotenv>=1.1.0` — `.env` file loading
- `pydantic>=2.11.0` — data validation

**Separate virtualenv** (`requirements-openai-agents.txt`):

- `openai-agents>=0.22.3` — OpenAI Agents SDK with `ComputerTool`/CUA, `ShellTool`, `ApplyPatchTool`
- Requires `openai>=3.0` which conflicts with `browser-use` (pins `openai==2.26.0`)

Install the Agents SDK in a separate venv:
```bash
python -m venv .venv-agents && source .venv-agents/bin/activate
pip install -r requirements-openai-agents.txt
python -m playwright install chromium
```

### Running the app

```bash
streamlit run streamlit_app.py --server.headless true --server.port 8501
```

- The app serves on port **8501**.
- The `--server.headless true` flag is required in headless/cloud environments.
- An **OpenAI API key** is required for Q&A functionality (enter via UI or set in `.env`).

### Running demos

All demo scripts load keys from `.env` via `python-dotenv`. Copy `.env.example` to `.env` first:

```bash
cp .env.example .env   # then fill in your keys
```

**Browser-Use agent** (requires `OPENAI_API_KEY` for full agent; runs Playwright smoke test without):
```bash
python scripts/browser_agent_demo.py
```

**CUA demo** (requires `OPENAI_API_KEY` — uses `computer-use-preview` model):
```bash
python scripts/cua_demo.py
```

**Agents SDK CUA** (requires separate venv + `OPENAI_API_KEY`):
```bash
source .venv-agents/bin/activate
python scripts/agents_sdk_cua_demo.py
```

### Browser-Use skills reference

`browser-use` provides an `Agent` class that drives a headless Chromium browser:

```python
from browser_use import Agent, Browser, ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
browser = Browser(headless=True)
agent = Agent(task="Find the top HN story", llm=llm, browser=browser)
result = await agent.run()
```

Key classes:
- `Agent` — orchestrates multi-step browser tasks
- `Browser` — Playwright browser wrapper (accepts `headless`, `cdp_url`, `viewport`, etc. directly)
- `ChatOpenAI`, `ChatAnthropic`, `ChatGoogle`, `ChatBrowserUse` — LLM adapters
- `Tools` / `@tools.action` — custom tool registration for agents
- `BrowserSession` — injected into custom tools for direct page access

### CUA (Computer-Use Agent) skills reference

The CUA pattern uses OpenAI's `computer-use-preview` model (or `gpt-5.6` in Agents SDK) to see screenshots and emit actions:

1. Capture a screenshot → send as base64 image
2. Model returns `computer_call` with actions (click, type, scroll, keypress)
3. Execute actions in Playwright → capture new screenshot → loop

Supported action types: `click`, `double_click`, `type`, `keypress`, `scroll`, `move`, `wait`, `drag`, `screenshot`.

### Global integration tools and connected agent

**Global integration tools** are user-level MCP servers in `~/.cursor/mcp.json`. **Project integration tools** live in `.cursor/mcp.json`.

| Scope | Location | Use for |
|-------|----------|---------|
| Global | `~/.cursor/mcp.json` | Personal tools (e.g. GitHub, Notion) across all repos |
| Project | `.cursor/mcp.json` | Team-shared tools for this repo |
| Cloud Agent | [cursor.com/agents](https://cursor.com/agents) MCP dropdown | Cloud runs |

**Local setup:**
1. Run `./scripts/setup-mcp.sh` (creates `.env` from `.env.example`).
2. Set `HF_TOKEN` in `.env`.
3. Reload Cursor and confirm **huggingface** appears under Settings -> Tools & MCP.

**Cloud Agent setup:** Add secrets (`HF_TOKEN`, `OPENAI_API_KEY`, etc.) at [cursor.com/agents](https://cursor.com/agents).

### Cursor Agent CLI

Local and CI workflows can use the same Agent as the editor via the [Cursor CLI](https://cursor.com/docs/cli/overview).

**Install / update:**

```bash
./scripts/setup-cursor-cli.sh
# or: curl https://cursor.com/install -fsS | bash
export PATH="$HOME/.local/bin:$PATH"
agent update
agent --version
```

**Authenticate:** `agent login`, or set `CURSOR_API_KEY`.

**Modes** (same as the editor):

| Mode | How to start | Behavior |
|------|--------------|----------|
| Agent | `agent` (default) | Full tools — edit, shell, search |
| Plan | `agent --plan` / `--mode=plan` / `/plan` | Design approach; clarifying questions; no coding until you agree |
| Ask | `agent --mode=ask` / `/ask` | Read-only Q&A over the codebase |

Interactive tips: `Shift+Tab` rotates modes; `@` attaches files; `/summarize` frees context; prepend `&` to hand off to [Cloud Agent](https://cursor.com/agents); `-w` / `--worktree` edits in an isolated Git worktree under `~/.cursor/worktrees/`.

**Non-interactive / scripts:**

```bash
agent -p "summarize streamlit_app.py"
agent -p --output-format json "list MCP servers configured for this repo"
```

The CLI loads project [`.cursor/mcp.json`](.cursor/mcp.json), [`.cursor/rules`](.cursor/rules) (if present), and this `AGENTS.md` the same way the editor does.

### Notes

- No automated tests or linting are configured.
- No build step required — all scripts run directly from source.
- Playwright Chromium must be installed: `python -m playwright install chromium && python -m playwright install-deps chromium`.
