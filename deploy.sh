#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f .env ]]; then
  echo "Copy .env.example to .env and fill in the values." >&2
  exit 1
fi

sudo docker compose up -d --build
