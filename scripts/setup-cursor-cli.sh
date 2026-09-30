#!/usr/bin/env bash
# Install or update Cursor Agent CLI (https://cursor.com/docs/cli/installation)
set -euo pipefail

curl https://cursor.com/install -fsS | bash

export PATH="$HOME/.local/bin:$PATH"

if ! command -v agent >/dev/null 2>&1; then
  echo "agent not on PATH. Add: export PATH=\"\$HOME/.local/bin:\$PATH\"" >&2
  exit 1
fi

agent update || true
echo
agent --version
agent about 2>/dev/null | head -20 || true
echo
echo "Next steps:"
echo "  agent login          # authenticate (or set CURSOR_API_KEY)"
echo "  agent                # interactive Agent mode"
echo "  agent --plan \"...\"   # Plan mode"
echo "  agent --mode=ask \"...\"  # Ask (read-only) mode"
echo "  agent -p \"...\"       # non-interactive / scripts"
