#!/usr/bin/env bash
set -euo pipefail

DOMAIN="${1:-ctf.example.com}"
BASE_DIR="$(pwd)"
DYN_DIR="${BASE_DIR}/data/traefik"
CERTS_DIR="${BASE_DIR}/data/certs"
CA_CN="CTF Platform Internal Root CA"
DAYS_CA=3650
DAYS_LEAF=365

mkdir -p "${CERTS_DIR}" "${DYN_DIR}"

CA_KEY="${CERTS_DIR}/ctf-platform-rootCA.key"
CA_CRT="${CERTS_DIR}/ctf-platform-rootCA.crt"
LEAF_KEY="${CERTS_DIR}/ctf-platform.key"
LEAF_CSR="${CERTS_DIR}/ctf-platform.csr"
LEAF_CRT="${CERTS_DIR}/ctf-platform.crt"

echo "[*] Gerando CA nova: ${CA_CN}"
cat > "${CERTS_DIR}/ca.conf" <<EOF
[ req ]
default_md = sha256
distinguished_name = dn
x509_extensions = v3_ca
prompt = no
[ dn ]
C = BR
O = CTF Platform
CN = ${CA_CN}
[ v3_ca ]
basicConstraints = critical, CA:true, pathlen:0
keyUsage = critical, keyCertSign, cRLSign
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
EOF

echo "[*] Gerando config do servidor p/ ${DOMAIN} (inclui wildcard)"
cat > "${CERTS_DIR}/server.conf" <<EOF
[ req ]
default_md = sha256
prompt = no
distinguished_name = dn
req_extensions = v3_req
[ dn ]
C = BR
O = CTF Platform
CN = ${DOMAIN}
[ v3_req ]
basicConstraints = CA:false
keyUsage = critical, digitalSignature
extendedKeyUsage = serverAuth
subjectKeyIdentifier = hash
subjectAltName = @alt
[ alt ]
DNS.1 = ${DOMAIN}
DNS.2 = *.${DOMAIN}
EOF

# 1) CA
openssl ecparam -name prime256v1 -genkey -noout -out "${CA_KEY}"
openssl req -x509 -new -key "${CA_KEY}" -sha256 -days "${DAYS_CA}" \
  -out "${CA_CRT}" -config "${CERTS_DIR}/ca.conf"

# 2) Cert do host
openssl ecparam -name prime256v1 -genkey -noout -out "${LEAF_KEY}"
openssl req -new -key "${LEAF_KEY}" -out "${LEAF_CSR}" -config "${CERTS_DIR}/server.conf"
openssl x509 -req -in "${LEAF_CSR}" -CA "${CA_CRT}" -CAkey "${CA_KEY}" \
  -CAcreateserial -out "${LEAF_CRT}" -days "${DAYS_LEAF}" -sha256 \
  -extfile "${CERTS_DIR}/server.conf" -extensions v3_req

# 3) Traefik tls.yml
cat > "${DYN_DIR}/tls.yml" <<EOF
tls:
  certificates:
    - certFile: /certs/ctf-platform.crt
      keyFile: /certs/ctf-platform.key
  options:
    secure-min-tls12:
      minVersion: VersionTLS12
      sniStrict: true
EOF

echo "[+] CA SHA256: $(openssl x509 -in "${CA_CRT}" -noout -fingerprint -sha256)"
echo "[+] SAN da folha:"
openssl x509 -in "${LEAF_CRT}" -noout -ext subjectAltName

# 4) Tenta recarregar o Traefik
if command -v docker >/dev/null 2>&1; then
  if docker compose ps traefik >/dev/null 2>&1; then
    echo "[*] Recarregando Traefik (docker compose up -d traefik)"
    docker compose up -d traefik
  elif command -v docker-compose >/dev/null 2>&1; then
    echo "[*] Recarregando Traefik (docker-compose up -d traefik)"
    docker-compose up -d traefik
  else
    echo "[i] Docker Compose não detectado; reinicie o container do Traefik manualmente."
  fi
fi

echo
echo "[✓] Pronto."
echo "    -> Distribua aos clientes: ${CA_CRT}"
echo "    -> O Traefik já deve estar servindo: ${LEAF_CRT} + ${LEAF_KEY}"
