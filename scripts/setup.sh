#!/usr/bin/env sh

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create venv
uv venv

# Activate venv
. .venv/bin/activate

# Install dependencies using uv
uv pip install -r requirements.txt
