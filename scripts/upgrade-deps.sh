#!/usr/bin/env bash
# Upgrade project Python environments and optional Node tooling.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> Ensuring python3-venv is available"
if ! python3 -m venv --help >/dev/null 2>&1; then
  echo "Install python3-venv first (e.g. sudo apt install python3.12-venv)" >&2
  exit 1
fi

echo "==> Primary venv (.venv)"
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -U pip setuptools wheel
pip install -U -r requirements.txt
python -m playwright install chromium || true
deactivate

echo "==> Agents SDK venv (.venv-agents)"
python3 -m venv .venv-agents
# shellcheck disable=SC1091
source .venv-agents/bin/activate
pip install -U pip setuptools wheel
pip install -U -r requirements-openai-agents.txt
python -m playwright install chromium || true
deactivate

if command -v npm >/dev/null 2>&1; then
  echo "==> Jules CLI (user-local npm prefix)"
  PREFIX="${JULES_INSTALL_PREFIX:-$HOME/.local}"
  npm install -g @google/jules@latest --prefix "$PREFIX" || true
fi

echo
echo "Done. Activate with: source .venv/bin/activate"
echo "Agents SDK:          source .venv-agents/bin/activate"
