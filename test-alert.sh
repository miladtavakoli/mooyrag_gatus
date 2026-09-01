#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

API_KEY=$(grep '^SMS_WEBHOOK_API_KEY=' .env | cut -d= -f2-)
NETWORK=$(sudo docker inspect -f '{{range $k,$v := .NetworkSettings.Networks}}{{$k}}{{end}}' sms-webhook)

sudo docker run --rm \
  --network "$NETWORK" \
  curlimages/curl \
  -sS -X POST \
  http://sms-webhook:8000/alert \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $API_KEY" \
  -d "{\"message\":\"${1:-Mooyrag uptime test}\"}"
echo
