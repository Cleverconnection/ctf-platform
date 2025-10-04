#!/usr/bin/env bash
# Interactive deleter para Docker Registry v2.
# Lista repositórios, permite escolher um por número, apaga todas as tags/manifests
# desse repositório e (opcionalmente) roda garbage-collect no container do registry.
# Baseado na API HTTP v2 do Registry (/_catalog, /tags/list, DELETE por digest).

set -Eeuo pipefail

REGISTRY_URL="${REGISTRY_URL:-http://localhost:5000}"
PAGE_SIZE="${PAGE_SIZE:-1000}"
ACCEPT_HEADER="${ACCEPT_HEADER:-application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.v1+json, application/vnd.docker.distribution.manifest.v2+json, application/vnd.oci.image.index.v1+json, application/vnd.docker.distribution.manifest.list.v2+json}"

require() { command -v "$1" >/dev/null || { echo "Erro: comando '$1' não encontrado."; exit 1; }; }
require curl
require jq

# Verifica acesso básico ao registry
if ! curl -fsS -o /dev/null "$REGISTRY_URL/v2/"; then
  echo "Erro: não consegui acessar $REGISTRY_URL/v2/."
  echo "Dica: se estiver dentro de um container da mesma rede do Compose, exporte:"
  echo "      REGISTRY_URL=http://registry:5000"
  exit 1
fi

fetch_catalog() {
  local last="" url headers body
  local -a repos=()
  local n="$PAGE_SIZE"
  while :; do
    url="$REGISTRY_URL/v2/_catalog?n=$n"
    [[ -n "$last" ]] && url="$url&last=$last"
    headers="$(mktemp)"; body="$(mktemp)"
    curl -fsS -D "$headers" "$url" -o "$body"
    mapfile -t arr < <(jq -r '.repositories[]?' "$body")
    repos+=("${arr[@]}")
    # paginação (Link: </v2/_catalog?...>; rel="next")
    local link
    link="$(tr -d '\r' <"$headers" | awk 'tolower($1)=="link:"{print $0}' | head -n1 || true)"
    rm -f "$headers" "$body"
    if [[ -z "$link" ]] || [[ "$link" != *'rel="next"'* ]]; then
      break
    fi
    last="$(sed -n 's/.*[?&]last=\([^&>]*\).*/\1/p' <<< "$link" | head -n1)"
    [[ -z "$last" ]] && break
  done
  printf '%s\n' "${repos[@]}"
}

list_tags() {
  local repo="$1"
  curl -fsS "$REGISTRY_URL/v2/$repo/tags/list" | jq -r '.tags[]?' || true
}

digest_for_tag() {
  local repo="$1" tag="$2"
  # 1) HEAD: retorna o header Docker-Content-Digest na maioria dos setups
  local digest
  digest="$(curl -fsSI -H "Accept: $ACCEPT_HEADER" "$REGISTRY_URL/v2/$repo/manifests/$tag" \
            | tr -d '\r' | awk -F': ' '/Docker-Content-Digest:/ {print $2}' | tail -n1 || true)"
  # 2) Fallback: GET (algumas instâncias não retornam no HEAD)
  if [[ -z "${digest:-}" ]]; then
    digest="$(curl -fsS -D - -H "Accept: $ACCEPT_HEADER" "$REGISTRY_URL/v2/$repo/manifests/$tag" -o /dev/null \
              | tr -d '\r' | awk -F': ' '/Docker-Content-Digest:/ {print $2}' | tail -n1 || true)"
  fi
  [[ -n "${digest:-}" ]] && printf '%s' "$digest"
}

delete_manifest_by_digest() {
  local repo="$1" digest="$2"
  local code
  code="$(curl -s -o /dev/null -w '%{http_code}' -X DELETE "$REGISTRY_URL/v2/$repo/manifests/$digest")"
  [[ "$code" == "202" ]] || { echo "Falha ao deletar $repo@$digest (HTTP $code)"; return 1; }
}

run_gc() {
  local container="${REGISTRY_CONTAINER:-registry}"
  # Tenta caminhos comuns do binário dentro do container
  if docker exec "$container" /bin/registry --version >/dev/null 2>&1; then
    docker exec -it "$container" /bin/registry garbage-collect /etc/docker/registry/config.yml
  elif docker exec "$container" registry --version >/dev/null 2>&1; then
    docker exec -it "$container" registry garbage-collect /etc/docker/registry/config.yml
  else
    echo "Não encontrei o binário 'registry' dentro do container '$container'."
    echo "Rode manualmente: docker exec -it <container> /bin/registry garbage-collect /etc/docker/registry/config.yml"
    return 1
  fi
}

main() {
  echo "Conectando ao registry: $REGISTRY_URL"
  mapfile -t repos < <(fetch_catalog)
  if [[ "${#repos[@]}" -eq 0 ]]; then
    echo "Nenhum repositório encontrado."
    exit 0
  fi

  echo "Repositórios encontrados:"
  local i=1
  for r in "${repos[@]}"; do
    printf "  [%d] %s\n" "$i" "$r"
    ((i++))
  done
  echo

  read -rp "Digite o número do repositório que deseja DELETAR: " choice
  if [[ -z "${choice:-}" ]] || ! [[ "$choice" =~ ^[0-9]+$ ]]; then
    echo "Entrada inválida."; exit 1
  fi
  local idx=$((choice-1))
  if (( idx < 0 || idx >= ${#repos[@]} )); then
    echo "Número fora do intervalo."; exit 1
  fi

  local repo="${repos[$idx]}"
  echo ">>> Selecionado: $repo"
  read -rp "Confirma DELETAR todas as tags/manifests do repositório '$repo'? (y/N): " yn
  if [[ "${yn:-}" != "y" && "${yn:-}" != "Y" ]]; then
    echo "Abortado."; exit 0
  fi

  mapfile -t tags < <(list_tags "$repo")
  if [[ "${#tags[@]}" -eq 0 ]]; then
    echo "Sem tags em '$repo' (nada para deletar)."
  else
    echo "Tags encontradas: ${tags[*]}"
    local deleted=0 failed=0
    for tag in "${tags[@]}"; do
      printf "  - Resolvendo digest de %s:%s ... " "$repo" "$tag"
      local digest; digest="$(digest_for_tag "$repo" "$tag" || true)"
      if [[ -z "${digest:-}" ]]; then
        echo "ERRO (Docker-Content-Digest ausente)."
        ((failed++)); continue
      fi
      echo "$digest"
      printf "    Deletando manifest... "
      if delete_manifest_by_digest "$repo" "$digest"; then
        echo "OK (202)"; ((deleted++))
      else
        echo "ERRO"; ((failed++))
      fi
    done
    echo "Resumo: deletados=$deleted, falhas=$failed"
  fi

  echo
  read -rp "Rodar garbage-collect no container do registry agora? (y/N): " gc
  if [[ "${gc:-}" == "y" || "${gc:-}" == "Y" ]]; then
    if command -v docker >/dev/null 2>&1; then
      run_gc || true
    else
      echo "Docker CLI não encontrado; não foi possível rodar o GC automaticamente."
    fi
  fi

  echo "Concluído."
}

main "$@"
