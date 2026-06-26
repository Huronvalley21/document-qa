## Cursor Cloud specific instructions

Single-file Streamlit app (`streamlit_app.py`) for document question answering using OpenAI. See `README.md` for basic setup commands.

### PATH setup

pip installs scripts to `~/.local/bin`. Ensure it's on PATH before running `streamlit`:

```
export PATH="$HOME/.local/bin:$PATH"
```

### Global integration tools and connected agent

**Global integration tools** are user-level MCP (Model Context Protocol) servers in `~/.cursor/mcp.json`. They are available in every project on your machine. **Project integration tools** live in [`.cursor/mcp.json`](.cursor/mcp.json) and are shared with the team when committed to git.

A **connected agent** is an Agent session where MCP servers are installed, authenticated, and enabled. The agent can call those tools during tasks (with approval unless allowlisted). Project and global configs are merged; if the same server name exists in both, the project config wins.

| Scope | Location | Use for |
| --- | --- | --- |
| Global | `~/.cursor/mcp.json` | Personal tools (e.g. GitHub, Notion) across all repos |
| Project | `.cursor/mcp.json` | Team-shared tools for this repo |
| Cloud Agent | [cursor.com/agents](https://cursor.com/agents) MCP dropdown | Team/cloud runs; not your local `~/.cursor/mcp.json` |

This repo includes a project-level Hugging Face MCP server so agents can search Hub models/datasets, fetch docs, and explore LLM tooling relevant to document QA.

**Local setup (do not commit secrets):**

1. Run `./scripts/setup-mcp.sh` (creates `.env` from [`.env.example`](.env.example)).
2. Set `HF_TOKEN` in `.env` using a token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens), or paste a config from [huggingface.co/settings/mcp](https://huggingface.co/settings/mcp).
3. Reload Cursor and confirm **huggingface** appears under Settings → Tools & MCP.
4. In Agent chat, check **Available Tools** or ask the agent to list MCP tools.

[`.cursor/mcp.json`](.cursor/mcp.json) uses `${env:HF_TOKEN}` and loads `.env` via `envFile` so tokens stay out of git.

**Cloud Agent setup:** Add `HF_TOKEN` as a Cloud Agent secret at [cursor.com/agents](https://cursor.com/agents), or use team MCP already configured there (e.g. Huggingface-skills).

### Running the app

```
streamlit run streamlit_app.py --server.headless true --server.port 8501
```

- Port **8501**. The `--server.headless true` flag is required in cloud/headless environments.
- **OpenAI API key** is required for Q&A functionality — entered via the UI or stored in `.streamlit/secrets.toml` (gitignored). If the `OPENAI_API_KEY` env var is set, you can pre-configure it by creating `.streamlit/secrets.toml`:
  ```
  OPENAI_API_KEY = "sk-..."
  ```

### Key facts

- No automated tests or linting configured.
- No build step — runs directly from source.
- No database or external services beyond the OpenAI API.
- Python 3.12 is available in the cloud environment; the app is compatible with Python 3.9+.
