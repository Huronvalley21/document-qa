## Cursor Cloud specific instructions

Single-file Streamlit app (`streamlit_app.py`) for document question answering using OpenAI. See `README.md` for basic setup commands.

### PATH setup

pip installs scripts to `~/.local/bin`. Ensure it's on PATH before running `streamlit`:

```
export PATH="$HOME/.local/bin:$PATH"
```

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
