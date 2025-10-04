#!/usr/bin/env bash
set -euo pipefail

CTFD_URL="http://localhost:8000"
API_TOKEN="ctfd_6f9876fb16277049367b3397755626c54ea1025b94046fc0042683f0eac31ae8"

# Função para aplicar patch
update_challenge () {
  local ID="$1"
  local SLUG="$2"

  echo ">>> Atualizando challenge ID=$ID (slug=$SLUG)"
  curl -s -w "\nHTTP_CODE:%{http_code}\n" -X PATCH \
    -H "Authorization: Bearer $API_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"state\":\"visible\",\"connection_info\":\"http://${SLUG}:8080\",\"image\":\"ctf/${SLUG}:latest\"}" \
    "$CTFD_URL/api/v1/challenges/$ID" | sed -n '1,200p'
}

# M01 - MFA sem Ordem
update_challenge 79 "mfa-sem-ordem"

# M02 - Token Confuso
update_challenge 80 "token-confuso"

