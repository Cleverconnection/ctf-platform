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
O=CTF Platform
CN=CTF Platform Internal Root CA
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
O=CTF Platform
CN=ctf.example.com
[ v3_req ]
basicConstraints=CA:false
keyUsage=critical,digitalSignature
extendedKeyUsage=serverAuth
subjectAltName=@alt
[ alt ]
DNS.1=ctf.example.com
# Se o spawner criar subdomínios por desafio, use também:
# DNS.2=*.ctf.example.com
EOF

openssl ecparam -name prime256v1 -genkey -noout -out ctf-platform.key
openssl req -new -key ctf-platform.key -out ctf-platform.csr -config server.conf
openssl x509 -req -in ctf-platform.csr -CA rootCA.crt -CAkey rootCA.key \
  -CAcreateserial -out ctf-platform.crt -days 365 -sha256 \
  -extfile server.conf -extensions v3_req
