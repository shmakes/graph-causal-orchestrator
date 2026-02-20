#!/usr/bin/env bash
# Install latest stable Python 3 with pyenv and set it locally for this project only.
# Other projects are unaffected (pyenv uses .python-version in this directory).
# Run from project root: bash scripts/setup-pyenv-python.sh
# Requires: pyenv, build dependencies (see https://github.com/pyenv/pyenv/wiki#suggested-build-environment)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

if ! command -v pyenv &>/dev/null; then
  echo "pyenv not found. Install it first: https://github.com/pyenv/pyenv#installation"
  exit 1
fi

# Latest stable 3.13.x (skip -t / -dev suffixes)
VERSION="$(pyenv install --list | grep -E '^\s+3\.13\.[0-9]+$' | sed 's/^[[:space:]]*//' | sort -V | tail -1)"

if [ -z "$VERSION" ]; then
  echo "Could not detect latest 3.13.x. Try: pyenv install 3.13.12"
  exit 1
fi

echo "Installing Python $VERSION (this may take a few minutes)..."
pyenv install -s "$VERSION"

echo "Setting Python $VERSION for this project only (.python-version)..."
pyenv local "$VERSION"

echo ""
echo "Done. This project will use Python $VERSION; other projects are unchanged."
echo "Verify: python --version && which python"
