#!/bin/bash
# Caminho base para os desafios médios
BASE_DIR="."

# Lista dos diretórios de desafios médios (prefixo M)
# Ajuste a lista caso adicione novos desafios
MEDIO_CHALLENGES=(
  "M01_auth_bypass_logic"
  "M02_jwt_kid_attack"
  "M06_xml_dos_xxe_combo"
  "M10_ssrf_s3_misuse"
  "M11_confd_leak"
  "M12_otp_bypass"
  "M13_csrf_api"
  "M14_account_merge_bug"
  "M15_ssrf_internal_metadata"
  "M16_race_balance_check"
  "M17_timing_attack"
  "M18_insecure_file_serve"
  "M19_authorization_header_splitting"
  "M20_log_forensics_tamper"
)

echo "Registrando desafios médios no .ctf/config..."
for chall in "${MEDIO_CHALLENGES[@]}"; do
  # Diretório relativo ao desafio
  DIR="$BASE_DIR/$chall"
  if [ -d "$DIR" ]; then
    echo "  -> registrando $DIR"
    ctf challenge add "$DIR" || true
  else
    echo "  !! diretório $DIR não encontrado; verifique o nome"
  fi
done

echo "Validando sintaxe (lint/verify)..."
ctf challenge lint
ctf challenge verify

echo "Instalando (publicando) desafios médios..."
# Use a flag --hidden se quiser publicá‑los inicialmente como ocultos
ctf challenge install

echo "Processo concluído. Verifique os desafios no painel do CTFd."
