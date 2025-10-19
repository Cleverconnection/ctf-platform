#!/bin/bash
set -euo pipefail

COMPOSE_CMD=${COMPOSE_CMD:-docker compose}
SERVICE=${SERVICE:-chall-manager}
SCENARIOS_DIR=/scenarios

echo "[*] Listando desafios disponíveis no container..."
mapfile -t SCENARIOS < <($COMPOSE_CMD exec -T "$SERVICE" bash -c "ls -1 $SCENARIOS_DIR")

if [ ${#SCENARIOS[@]} -eq 0 ]; then
  echo "Nenhum desafio encontrado em $SCENARIOS_DIR dentro do container."
  exit 1
fi

# Exibe opções numeradas
for i in "${!SCENARIOS[@]}"; do
  printf "%2d) %s\n" $((i+1)) "${SCENARIOS[$i]}"
done

# Pergunta ao usuário
read -rp "Escolha o número do desafio que deseja destruir: " choice
if ! [[ "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -lt 1 ] || [ "$choice" -gt ${#SCENARIOS[@]} ]]; then
  echo "Opção inválida."
  exit 1
fi

CHALLENGE=${SCENARIOS[$((choice-1))]}
WORKDIR="$SCENARIOS_DIR/$CHALLENGE"

echo "[*] Destruindo instância do desafio: $CHALLENGE"
$COMPOSE_CMD exec -T -w "$WORKDIR" "$SERVICE" python3 destroy.py

echo "[+] Instância do desafio '$CHALLENGE' destruída (destroy.py executado)."
