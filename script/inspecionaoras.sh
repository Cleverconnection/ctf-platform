# Se for registry sem TLS:
ORAS_FLAGS="--plain-http"

# 1) Manifest do :2
oras manifest fetch $ORAS_FLAGS registry:5000/web-102:2 | jq .

# 2) Listar camadas (mídia + título + digest + tamanho)
oras manifest fetch $ORAS_FLAGS registry:5000/web-102:2 \
| jq -r '.layers[] | [.mediaType, (.annotations["org.opencontainers.image.title"] // ""), .digest, .size] | @tsv'

# 3) (Opcional) baixar a 1ª layer p/ ver o conteúdo
DIGEST=$(oras manifest fetch $ORAS_FLAGS registry:5000/web-102:2 | jq -r '.layers[0].digest')
oras blob fetch $ORAS_FLAGS registry:5000/web-102:2 "$DIGEST" > /tmp/web-102.layer
file /tmp/web-102.layer
# Se for .tar.gz:
tar tzf /tmp/web-102.layer | head

