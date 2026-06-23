#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$ROOT/.env"
EXAMPLE_FILE="$ROOT/.env.example"

if [[ -f "$ENV_FILE" ]] && rg -q '^HF_TOKEN=.+$' "$ENV_FILE" 2>/dev/null; then
  echo "HF_TOKEN already set in $ENV_FILE"
  exit 0
fi

if [[ -n "${HF_TOKEN:-}" ]]; then
  printf 'HF_TOKEN=%s\n' "$HF_TOKEN" > "$ENV_FILE"
  chmod 600 "$ENV_FILE"
  echo "Wrote HF_TOKEN to $ENV_FILE from environment"
  exit 0
fi

if [[ ! -f "$EXAMPLE_FILE" ]]; then
  echo "Missing $EXAMPLE_FILE" >&2
  exit 1
fi

cp "$EXAMPLE_FILE" "$ENV_FILE"
chmod 600 "$ENV_FILE"
echo "Created $ENV_FILE"
echo "Edit it and set HF_TOKEN, then reload Cursor (Settings → Tools & MCP)."
