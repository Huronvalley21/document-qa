## Cursor Cloud specific instructions

This is a single-file Streamlit app (`streamlit_app.py`) for document question answering using OpenAI's GPT-3.5-turbo. See `README.md` for basic setup.

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

- The app serves on port **8501**.
- The `--server.headless true` flag is required in headless/cloud environments to suppress the browser-open prompt.
- An **OpenAI API key** is required for question-answering functionality. It can be entered via the UI text input or stored in `.streamlit/secrets.toml` (gitignored).

### Notes

- There are no automated tests or linting configured in this repository.
- No build step is required — the app runs directly from source.
- No database or external services are needed beyond the OpenAI API.
