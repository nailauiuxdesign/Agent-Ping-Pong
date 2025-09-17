#!/usr/bin/env bash
set -e

PYTHON_SCRIPT="main.py"
SCRIPT_DIR=$(dirname "$(realpath "$0" 2>/dev/null || readlink -f "$0" 2>/dev/null || echo "$0")")
PROJECT_DIR="$SCRIPT_DIR"
cd "$PROJECT_DIR" || exit 1
echo "Running $PYTHON_SCRIPT..."
uv run "$PYTHON_SCRIPT"
