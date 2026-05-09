## Cursor Cloud specific instructions

This is a single-file Streamlit app (`streamlit_app.py`) for document question answering using OpenAI's GPT-3.5-turbo. See `README.md` for basic setup.

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
