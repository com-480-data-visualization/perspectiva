#!/usr/bin/env bash
# Run once after cloning: bash setup.sh
#
# What it does:
#   1. Creates a .venv if one doesn't exist
#   2. Installs all dependencies from requirements.txt
#   3. Installs nbstripout as a git filter
#   4. Configures git to use the project hooks in .githooks/

set -e

REPO_ROOT=$(cd "$(dirname "$0")" && pwd)

# --- 1. Create .venv if it doesn't exist ---
if [ ! -d "$REPO_ROOT/.venv" ]; then
    echo "[setup] Creating .venv..."
    python3 -m venv "$REPO_ROOT/.venv"
else
    echo "[setup] .venv already exists, skipping creation."
fi

source "$REPO_ROOT/.venv/bin/activate"

# --- 2. Install dependencies ---
echo "[setup] Installing dependencies from requirements.txt..."
pip install --upgrade pip --quiet
pip install -r "$REPO_ROOT/requirements.txt" --quiet

# --- 3. Install nbstripout git filter ---
echo "[setup] Installing nbstripout git filter..."
nbstripout --install

# --- 4. Set git hooks path ---
echo "[setup] Configuring git hooks..."
git config core.hooksPath .githooks
chmod +x "$REPO_ROOT/.githooks/pre-commit"

echo ""
echo "Setup complete. Activate your environment with:"
echo "  source .venv/bin/activate"
