#!/bin/bash
set -euo pipefail

CID="${1:-}"; SID="${2:-}"
CM_ROOT_DEFAULT="/home/user/ctf/chall_tmp"
CM_ROOT="${CM_ROOT:-$CM_ROOT_DEFAULT}"
ALT_ROOT="${ALT_ROOT:-/opt/chall-manager/chall}"

if [[ -z "$CID" || -z "$SID" ]]; then
  echo "Uso: $0 <challenge_id> <source_id>" >&2
  exit 1
fi

# md5 do challenge_id
CHASH="$(printf %s "$CID" | md5sum | awk '{print $1}')"

# escolhe raiz que contem o hash
ROOT=""
for r in "$CM_ROOT" "$ALT_ROOT"; do
  if [[ -d "$r/$CHASH" ]]; then ROOT="$r"; break; fi
done

if [[ -z "$ROOT" ]]; then
  echo "CHASH=$CHASH"
  echo "ROOT="
  echo "CHALL_DIR="
  echo "CHALL_INFO_MISSING=1"
  exit 0
fi

CHALL_DIR="$ROOT/$CHASH"
CH_INFO="$CHALL_DIR/info.json"

if [[ ! -f "$CH_INFO" ]]; then
  echo "CHASH=$CHASH"
  echo "ROOT=$ROOT"
  echo "CHALL_DIR=$CHALL_DIR"
  echo "CHALL_INFO_MISSING=1"
  exit 0
fi

# Lê 'directory' e 'scenario' (separados por TAB para evitar quebra por espaços)
IFS=$'\t' read -r DIRECTORY SCENARIO < <(
  python3 - <<'PY' "$CH_INFO"
import json, sys
j = json.load(open(sys.argv[1]))
d = j.get('directory','')
s = j.get('scenario','')
print(f"{d}\t{s}")
PY
)

PROJECT_ID=""
if [[ -n "$DIRECTORY" ]]; then
  PROJECT_ID="$(basename "$DIRECTORY")"
fi

PROJ_DIR="$CHALL_DIR/$PROJECT_ID"
INST_DIR="$CHALL_DIR/instance/$SID"
DESTROY_PY="$PROJ_DIR/destroy.py"
OUTPUTS_JSON="$PROJ_DIR/outputs.json"

echo "CHASH=$CHASH"
echo "ROOT=$ROOT"
echo "CHALL_DIR=$CHALL_DIR"
echo "INST_DIR=$INST_DIR"
echo "PROJ_DIR=$PROJ_DIR"
echo "DESTROY_PY=$DESTROY_PY"
echo "OUTPUTS_JSON=$OUTPUTS_JSON"
echo "SCENARIO=$SCENARIO"
if [[ -d "$PROJ_DIR" ]]; then
  echo "PROJ_DIR_EXISTS=1"
else
  echo "PROJ_DIR_EXISTS=0"
fi
exit 0
