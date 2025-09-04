FROM ctferio/chall-manager:latest
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/chall-venv/bin:${PATH}"
# Dependências básicas
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-venv ca-certificates curl jq golang git \
  && rm -rf /var/lib/apt/lists/*

# Venv global + libs para Proxmox/HTTP
RUN python3 -m venv /opt/chall-venv && \
    /opt/chall-venv/bin/pip install --no-cache-dir proxmoxer requests
# Compila e instala o chall-manager-cli
RUN git clone https://github.com/ctfer-io/chall-manager.git /tmp/chall-manager-src && \
    cd /tmp/chall-manager-src/cmd/chall-manager-cli && \
    go build -o /usr/local/bin/chall-manager-cli && \
    rm -rf /tmp/chall-manager-src


WORKDIR /app

