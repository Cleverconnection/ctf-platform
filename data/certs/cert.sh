# 1) CA raiz (guarde rootCA.key com permissão 600)
openssl ecparam -name prime256v1 -genkey -noout -out rootCA.key
cat > ca.conf <<'EOF'
[ req ]
default_md=sha256
distinguished_name=dn
x509_extensions=v3_ca
prompt=no
[ dn ]
C=BR
O=CECYBER
CN=CECYBER Internal Root CA
[ v3_ca ]
basicConstraints=critical,CA:true,pathlen:0
keyUsage=critical,keyCertSign,cRLSign
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid:always,issuer
EOF
openssl req -x509 -new -key rootCA.key -sha256 -days 3650 -out rootCA.crt -config ca.conf

# 2) Cert do host (ECDSA P-256) com SAN obrigatório
cat > server.conf <<'EOF'
[ req ]
default_md=sha256
prompt=no
distinguished_name=dn
req_extensions=v3_req
[ dn ]
C=BR
O=CECYBER
CN=ctf-itau.cecyber.com
[ v3_req ]
basicConstraints=CA:false
keyUsage=critical,digitalSignature
extendedKeyUsage=serverAuth
subjectAltName=@alt
[ alt ]
DNS.1=ctf-itau.cecyber.com
# Se o spawner criar subdomínios por desafio, use também:
# DNS.2=*.ctf-itau.cecyber.com
EOF

openssl ecparam -name prime256v1 -genkey -noout -out ctf-itau.key
openssl req -new -key ctf-itau.key -out ctf-itau.csr -config server.conf
openssl x509 -req -in ctf-itau.csr -CA rootCA.crt -CAkey rootCA.key \
  -CAcreateserial -out ctf-itau.crt -days 365 -sha256 \
  -extfile server.conf -extensions v3_req
