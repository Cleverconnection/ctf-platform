#!/usr/bin/env bash
set -euo pipefail

echo "[delete_ctf_images] Removendo imagens antigas de desafios..."

# Lista de imagens (nome:tag ou ID)
IMAGES=(
  "ctf/e9_cors_wildcard:latest"
  "ctf/e8_upload_exec_hint:latest"
  "ctf/e7_xxe_simple:latest"
  "ctf/e6_sql_injection_basic:latest"
  "ctf/e20_rate_limit_none:latest"
  "ctf/e1_auth_weak_pwd:latest"
  "ctf/e19_file_download_path:latest"
  "ctf/e18_missing_tls_redirect:latest"
  "ctf/e17_password_reset_enum:latest"
  "ctf/e16_public_backup:latest"
  "ctf/e15_weak_crypto:latest"
  "ctf/e14_timestamp_replay:latest"
  "ctf/e13_log_injection:latest"
  "ctf/e12_query_creds:latest"
  "ctf/e11_info_headers:latest"
  "ctf/e10_exposed_swagger:latest"
)

for img in "${IMAGES[@]}"; do
  echo "[info] Removendo $img ..."
  docker rmi -f "$img" || echo "[warn] Não foi possível remover $img (pode já ter sido deletada)."
done

echo "[delete_ctf_images] Finalizado."

