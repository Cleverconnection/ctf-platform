#!/usr/bin/env bash
# build-all.sh
# Constrói imagens Docker para cada subdiretório que contenha um Dockerfile.
# Injeta a FLAG correta via --build-arg FLAG_ARG=...
# Variáveis:
#   CTF_PREFIX - prefixo para as imagens (default: "ctf")
#   ROOT_DIR   - diretório raiz com os desafios (default: "ctf_challenges_5")

set -u

CTF_PREFIX="${CTF_PREFIX:-ctf}"
ROOT_DIR="${ROOT_DIR:-ctf_challenges_5}"
DOCKER_CMD="${DOCKER_CMD:-docker}"
FAILURES=()

# Mapa: nome do diretório -> FLAG
declare -A FLAGS=(
  ["E1_auth_weak_pwd"]="ITAU2025{weak_passwords_ruin_security}"
  ["E2_jwt_noexp"]="ITAU2025{jwt_without_expiration}"
  ["E3_idor_account"]="ITAU2025{idor_bank_accounts}"
  ["E4_open_redirect"]="ITAU2025{ssrf_proxy_to_flag}"
  ["E5_file_read"]="ITAU2025{path_traversal_master}"
  ["E6_sql_injection_basic"]="ITAU2025{sqli_in_the_branch}"
  ["E7_xxe_simple"]="ITAU2025{xxe_into_core}"
  ["E8_upload_exec_hint"]="ITAU2025{predictable_upload_leak}"
  ["E9_cors_wildcard"]="ITAU2025{cors_wildcard_token}"
  ["E10_exposed_swagger"]="ITAU2025{swagger_spill}"
  ["E11_info_headers"]="ITAU2025{headers_tell_secrets}"
  ["E12_query_creds"]="ITAU2025{creds_in_query}"
  ["E13_log_injection"]="ITAU2025{logs_are_trust_issue}"
  ["E14_timestamp_replay"]="ITAU2025{timestamp_replay_attack}"
  ["E15_weak_crypto"]="ITAU2025{weak_crypto_modes}"
  ["E16_public_backup"]="ITAU2025{public_backup_flag}"
  ["E17_password_reset_enum"]="ITAU2025{reset_enum_abuse}"
  ["E18_missing_tls_redirect"]="ITAU2025{tls_redirect_missing}"
  ["E19_file_download_path"]="ITAU2025{file_download_traversal}"
  ["E20_rate_limit_none"]="ITAU2025{rate_limit_none}"
)

echo "Iniciando build para todos os subdiretórios em: ${ROOT_DIR}"
echo "Prefixo de imagens: ${CTF_PREFIX}"
echo

if [ ! -d "${ROOT_DIR}" ]; then
  echo "ERRO: diretório raiz '${ROOT_DIR}' não existe."
  exit 2
fi

shopt -s nullglob
for dir in "${ROOT_DIR}"/*; do
  [ -d "$dir" ] || continue
  rawname="$(basename "$dir")"

  # normalizar name para tag docker
  safe_name="$(echo "$rawname" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9._-]/_/g')"
  tag="${CTF_PREFIX}/${safe_name}:latest"

  dockerfile="$(find "$dir" -maxdepth 2 -type f -iname Dockerfile | head -n 1 || true)"
  if [ -z "$dockerfile" ]; then
    echo "SKIP: '$rawname' (nenhum Dockerfile encontrado)"
    continue
  fi

  flag="${FLAGS[$rawname]:-CTF{placeholder}}"

  echo "------------------------------------------------------------"
  echo "BUILD: diretório: $dir"
  echo "       Dockerfile: $dockerfile"
  echo "       Tag: $tag"
  echo "       FLAG: ${flag}"
  echo

  if ${DOCKER_CMD} build --build-arg FLAG_ARG="${flag}" -t "${tag}" "$dir"; then
    echo "OK: build concluído para ${tag}"
  else
    echo "FAIL: build falhou para ${tag}"
    FAILURES+=("${tag}")
  fi

  echo
done

echo "------------------------------------------------------------"
if [ ${#FAILURES[@]} -eq 0 ]; then
  echo "Todos os builds concluídos com sucesso."
  exit 0
else
  echo "Alguns builds falharam:"
  for f in "${FAILURES[@]}"; do
    echo "  - $f"
  done
  exit 1
fi

