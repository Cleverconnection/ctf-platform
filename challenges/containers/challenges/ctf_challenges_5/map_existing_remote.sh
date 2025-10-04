#!/bin/bash
set -euo pipefail

CFG=".ctf/config"
: "${CTFD_URL:?Defina CTFD_URL}"
: "${CTFD_SESSION:?Defina CTFD_SESSION}"

# 1) Backup do .ctf/config
cp -f "$CFG" ".ctf/config.bak.$(date +%s)"

# 2) Extrai somente a seção [config] do arquivo atual e descarta o resto
awk '
  BEGIN{copy=0}
  /^\[config\]/{print; copy=1; next}
  /^\[/{if(copy){exit}; next}
  {if(copy) print}
' "$CFG" > .ctf/config.header

# 3) Busca remotos (admin view) — somente leitura
REMOTE_JSON=$(mktemp)
curl -s -H "Cookie: session=$CTFD_SESSION" \
     "$CTFD_URL/api/v1/challenges?view=admin" > "$REMOTE_JSON"

# 4) Cria lista de nomes remotos
mapfile -t REMOTE_NAMES < <(jq -r '.data[].name' "$REMOTE_JSON")

# 5) Constrói nova seção [challenges] apenas com matches
echo "[challenges]" > .ctf/config.chals

found=0
for d in E* M*; do
  [ -d "$d" ] || continue
  [ -f "$d/challenge.yml" ] || continue
  # Extrai name: do YAML
  LOCAL_NAME=$(awk -F': ' '/^name:/{sub(/^name: */,""); gsub(/^"|\"$/,""); print}' "$d/challenge.yml")
  if printf '%s\n' "${REMOTE_NAMES[@]}" | grep -Fxq "$LOCAL_NAME"; then
    echo "./$d = ./$d" >> .ctf/config.chals
    echo "match: $LOCAL_NAME  ->  $d"
    found=$((found+1))
  fi
done

# 6) Junta cabeçalho + seção challenges e finaliza
cat .ctf/config.header .ctf/config.chals > .ctf/config

echo "✅ .ctf/config atualizado com $found mapeamentos remotos existentes (server intocado)."
echo "Backup em: $(ls -1t .ctf/config.bak.* | head -n1)"
