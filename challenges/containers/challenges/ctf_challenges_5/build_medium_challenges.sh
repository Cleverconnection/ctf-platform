#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="${BASE_DIR:-./}"
CT_IMAGE_PREFIX="${CT_IMAGE_PREFIX:-ctf}"
LOG_DIR="${LOG_DIR:-./build_logs}"
NO_CACHE="${NO_CACHE:-0}"

mkdir -p "$LOG_DIR"

# ---- Mapeamento Inglês → Português ----
declare -A NOME_PT
NOME_PT["M01_auth_bypass_logic"]="mfa-sem-ordem"
NOME_PT["M02_jwt_kid_attack"]="token-confuso"
NOME_PT["M03_ssrf_internal_svc"]="proxy-cego"
NOME_PT["M04_concurrent_transfer_race"]="corrida-transferencias"
NOME_PT["M05_payment_replay"]="pagamentos-replay"
NOME_PT["M06_xml_dos_xxe_combo"]="xml-explosivo"
NOME_PT["M07_insecure_deserialize"]="job-java-inseguro"
NOME_PT["M08_supply_chain_devops"]="exposicao-artefatos"
NOME_PT["M09_privilege_escalation_api"]="patch-indireto"
NOME_PT["M10_ssrf_s3_misuse"]="proxy-s3-interno"
NOME_PT["M11_confd_leak"]="vazamento-configuracao"
NOME_PT["M12_otp_bypass"]="otp-previsivel"
NOME_PT["M13_csrf_api"]="requisicoes-cruzadas"
NOME_PT["M14_account_merge_bug"]="fusao-curiosa"
NOME_PT["M15_ssrf_internal_metadata"]="metadados-abertos"
NOME_PT["M16_race_balance_check"]="saldo-negativo-corrida"
NOME_PT["M17_timing_attack"]="ataque-pelo-tempo"
NOME_PT["M18_insecure_file_serve"]="armazenamento-exposto"
NOME_PT["M19_authorization_header_splitting"]="cabecalho-quebrado"
NOME_PT["M20_log_forensics_tamper"]="evidencias-manipuladas"

# ---- Função de build ----
build_one() {
  local dir="$1"
  local name_pt="${NOME_PT[$(basename "$dir")]:-}"
  local tag="$CT_IMAGE_PREFIX/${name_pt}:latest"
  local logfile="$LOG_DIR/${name_pt}.log"

  if [ -z "$name_pt" ]; then
    echo "[SKIP] $(basename "$dir"): sem nome em português definido" | tee -a "$logfile"
    return 0
  fi

  if [ ! -f "$dir/Dockerfile" ] && [ ! -d "$dir/docker" ]; then
    echo "[SKIP] $(basename "$dir"): sem Dockerfile/docker dir" | tee -a "$logfile"
    return 0
  fi

  echo ">>> Build $(basename "$dir") → $tag"
  docker build -t "$tag" $([ "$NO_CACHE" -eq 1 ] && echo "--no-cache") "$dir" >"$logfile" 2>&1 \
    && echo "[OK] $tag" | tee -a "$logfile" \
    || echo "[ERR] falha em $(basename "$dir"), veja $logfile" | tee -a "$logfile"
}

# ---- Loop pelos M* ----
for d in "$BASE_DIR"/M*; do
  [ -d "$d" ] || continue
  build_one "$d"
done
