#!/usr/bin/env bash
set -euo pipefail

if [[ -f ".venv/bin/activate" ]]; then
  source .venv/bin/activate
fi

if [[ -f ".env.runtime" ]]; then
  source .env.runtime
fi

: "${OPENAI_API_KEY:?OPENAI_API_KEY is required}"
: "${SERPER_API_KEY:?SERPER_API_KEY is required}"

export PYTHONPATH="${PYTHONPATH:-$PWD}"

python main.py
