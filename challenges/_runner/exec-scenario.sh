#!/usr/bin/env bash
set -euo pipefail

export SCENARIO_ROOT="${SCENARIO_ROOT:-/scenarios}"
action="${ACTION:-create}"

# Resolve diretório do cenário (preferindo SCENARIO_DIR que o chall-manager passa)
if [ -n "${SCENARIO_DIR:-}" ]; then
  dir="$SCENARIO_DIR"
elif [ -n "${SCENARIO_NAME:-}" ]; then
  dir="$SCENARIO_ROOT/$SCENARIO_NAME"
elif [ -n "${SCENARIO_REFERENCE:-}" ]; then
  ref="${SCENARIO_REFERENCE##*/}"      # web-101:1.17
  slug="${ref%%:*}"                    # web-101
  dir="$SCENARIO_ROOT/$slug"
else
  echo "ERRO: defina SCENARIO_DIR ou SCENARIO_NAME ou SCENARIO_REFERENCE" >&2; exit 2
fi

[ -d "$dir" ] || { echo "ERRO: diretorio inexistente: $dir" >&2; exit 3; }
cd "$dir"

# Venv fora do diretório do cenário (evita incluir .venv no pacote)
hash_id=$(printf "%s" "$dir" | sha256sum | cut -c1-8)
VENV_BASE="${VENV_BASE:-/tmp/chall-venvs}"
VENV_DIR="$VENV_BASE/${hash_id}"
python3 -m venv "$VENV_DIR" 2>/dev/null || true
. "$VENV_DIR/bin/activate"

# Dependências opcionais do cenário
if [ -f requirements.txt ]; then
  pip -q install -r requirements.txt
fi

case "$action" in
  create)
    if [ -f create.py ]; then exec python3 create.py
    elif [ -x create.sh ]; then exec ./create.sh
    else echo "ERRO: faltou create.py|create.sh" >&2; exit 4
    fi
    ;;
  destroy)
    if [ -f destroy.py ]; then exec python3 destroy.py
    elif [ -x destroy.sh ]; then exec ./destroy.sh
    else echo "ERRO: faltou destroy.py|destroy.sh" >&2; exit 5
    fi
    ;;
  *)
    echo "ERRO: ACTION desconhecida: $action" >&2; exit 6
    ;;
esac
