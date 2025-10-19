#!/bin/bash
set -euo pipefail

COMPOSE_CMD=${COMPOSE_CMD:-docker compose}
SERVICE=${SERVICE:-chall-manager}
SCENARIOS_DIR=/scenarios

echo "[*] Listando desafios disponíveis no container..."
# pega apenas diretórios dentro de /scenarios
mapfile -t SCENARIOS < <($COMPOSE_CMD exec -T "$SERVICE" bash -c "ls -1 $SCENARIOS_DIR")

if [ ${#SCENARIOS[@]} -eq 0 ]; then
  echo "Nenhum desafio encontrado em $SCENARIOS_DIR dentro do container."
  exit 1
fi

# exibe opções numeradas
for i in "${!SCENARIOS[@]}"; do
  printf "%2d) %s\n" $((i+1)) "${SCENARIOS[$i]}"
done

# pergunta ao usuário
read -rp "Escolha o número do desafio que deseja compilar: " choice
if ! [[ "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -lt 1 ] || [ "$choice" -gt ${#SCENARIOS[@]} ]; then
  echo "Opção inválida."
  exit 1
fi

CHALLENGE=${SCENARIOS[$((choice-1))]}
WORKDIR="$SCENARIOS_DIR/$CHALLENGE"

echo "[*] Desafio selecionado: $CHALLENGE"
echo "[*] Limpando binário antigo..."
$COMPOSE_CMD exec -T -w "$WORKDIR" "$SERVICE" rm -f main || true

echo "[*] Compilando main.go dentro do container..."
$COMPOSE_CMD exec -T -w "$WORKDIR" "$SERVICE" go build -o main main.go

echo "[+] Build concluído para o desafio '$CHALLENGE'."
$COMPOSE_CMD exec -T -w "$WORKDIR" "$SERVICE" ls -lh main
