#!/bin/bash

# Exit immediately if any command exits with a non-zero status
set -e

echo "========================================================="
echo "⚙️  DataForge CLI - Initializing Automated Setup Pipeline"
echo "========================================================="

# 1. Verify if Python 3 is installed in the target Linux environment
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 could not be found in this Linux ecosystem."
    exit 1
fi

echo "➔ Instantiating Python virtual environment (.venv)..."
python3 -m venv .venv

echo "➔ Activating the target virtual environment..."
source .venv/bin/activate

echo "➔ Upgrading pip package manager implementation..."
pip install --upgrade pip

echo "➔ Compiling production dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️  Warning: The requirements.txt file was not detected in the workspace root."
fi

echo "========================================================="
echo "✅ Automated workspace configuration completed successfully!"
echo "To execute the CLI engine, run: source .venv/bin/activate && python main.py --debug"
echo "========================================================="
