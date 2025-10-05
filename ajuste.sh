#!/bin/bash
set -euo pipefail
# Script: ajuste.sh
# Função: substituir submódulos gitlink por diretórios reais no repositório

echo "========================================"
echo " 🔧 Iniciando limpeza de submódulos órfãos (.gitmodules ausente)"
echo "========================================"

# Confirma que estamos dentro de um repo git
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
  echo "❌ Este diretório não é um repositório git."
  exit 1
fi

# Lista de submódulos a converter
paths=(
  "challenges/containers/challenges"
  "challenges/oras"
  "challenges/wireshark"
  "ctfd/containers"
  "ctfd/ctfd-chall-manager.bkp"
  "ctfd/plugins/challenge_logging"
  "ctfd/plugins/containers"
  "ctfd/plugins/ctfd-chall-manager"
  "ctfd/themes/CTFD-odin-theme"
  "ctfd/themes/CTFd-Car-Hacking-Theme"
  "ctfd/themes/crimson-theme"
  "ctfd/themes/ctfd-neon-theme"
  "ctfd/themes/themes"
)

for path in "${paths[@]}"; do
  echo "🔹 Limpando $path"
  git rm -f "$path" 2>/dev/null || true
  mkdir -p "$path"
  echo "# Submódulo convertido — conteúdo deve ser populado manualmente se necessário" > "$path/README.txt"
done

git add -A
git commit -m "chore: vendorizar submódulos (substituir gitlinks por pastas locais)" || echo "⚠️ Nenhuma modificação detectada."
git push origin main

echo "✅ Conclusão: submódulos convertidos com sucesso."
