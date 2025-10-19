#!/bin/bash
set -euo pipefail

CID="${1:-}"; SID="${2:-}"
SC_ROOT="${SC_ROOT:-/home/user/ctf/challenges}"
LOCATE="${LOCATE:-/home/user/ctf/script/cm-locate.sh}"

if [[ -z "$CID" || -z "$SID" ]]; then
  echo "Uso: $0 <challenge_id> <source_id>" >&2
  exit 1
fi
if [[ ! -x "$LOCATE" ]]; then
  echo "cm-locate.sh não encontrado/executável em $LOCATE" >&2
  exit 2
fi

# Carrega variáveis emitidas pelo cm-locate.sh
eval "$("$LOCATE" "$CID" "$SID")"

if [[ "${PROJ_DIR_EXISTS:-0}" != "1" ]]; then
  echo "PROJ_DIR inexistente (instância ainda não materializada?): $PROJ_DIR" >&2
  exit 10
fi

# Deriva slug do cenário: registry:5000/web-102:2 -> web-102
SCEN_SLUG="$(python3 - <<'PY' "$SCENARIO"
import sys
s = sys.argv[1]
print(s.split('/')[-1].split(':')[0] if s else '')
PY
)"
if [[ -z "$SCEN_SLUG" ]]; then
  echo "Falha ao extrair slug do SCENARIO: $SCENARIO" >&2
  exit 3
fi

SRC_DESTROY="$SC_ROOT/$SCEN_SLUG/destroy.py"
if [[ ! -f "$SRC_DESTROY" ]]; then
  echo "destroy.py de origem não existe: $SRC_DESTROY" >&2
  exit 4
fi

install -m 0755 "$SRC_DESTROY" "$DESTROY_PY"
echo "[OK] Copiado: $SRC_DESTROY -> $DESTROY_PY"
