#!/bin/bash
set -euo pipefail

CONTAINER=itau-chall-manager-1
SCENARIOS_DIR=/scenarios

echo "[*] Listando desafios disponíveis no container..."
# pega apenas diretórios dentro de /scenarios
mapfile -t SCENARIOS < <(docker exec $CONTAINER bash -c "ls -1 $SCENARIOS_DIR")

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
docker exec -w "$WORKDIR" $CONTAINER rm -f main || true

echo "[*] Compilando main.go dentro do container..."
docker exec -w "$WORKDIR" $CONTAINER go build -o main main.go

echo "[+] Build concluído para o desafio '$CHALLENGE'."
docker exec -w "$WORKDIR" $CONTAINER ls -lh main
