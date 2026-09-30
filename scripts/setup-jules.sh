#!/usr/bin/env bash
# Install or update Google Jules CLI (async coding agent companion).
# Docs: https://jules.google/docs/cli/reference/
set -euo pipefail

PREFIX="${JULES_INSTALL_PREFIX:-$HOME/.local}"
BIN_DIR="$PREFIX/bin"

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required. Install Node.js first: https://nodejs.org/" >&2
  exit 1
fi

mkdir -p "$BIN_DIR"
echo "Installing/updating @google/jules to $PREFIX ..."
npm install -g @google/jules@latest --prefix "$PREFIX"

export PATH="$BIN_DIR:$PATH"

if ! command -v jules >/dev/null 2>&1; then
  echo "jules not on PATH. Add this to your shell profile:" >&2
  echo "  export PATH=\"$BIN_DIR:\$PATH\"" >&2
  exit 1
fi

echo
jules version
echo
echo "Next steps:"
echo "  1. Connect GitHub at https://jules.google (required once)"
echo "  2. Authenticate the CLI: jules login"
echo "  3. Verify: jules remote list --repo"
echo "  4. Start a task: jules new \"your task\" --repo OWNER/REPO"
