# ============================
#  Base CTFd
# ============================
FROM ghcr.io/ctfd/ctfd:3.8.0

USER root

# ============================
#  Dependências extras
# ============================
# - pipx para gerenciar ferramentas Python isoladas
# - nano, git, curl, jq para manutenção/admin
RUN apt-get update && apt-get install -y --no-install-recommends \
      pipx nano git curl jq \
    && rm -rf /var/lib/apt/lists/*

# Garantir que pipx binários fiquem no PATH
ENV PATH=/root/.local/bin:$PATH

# Instalar o ctfcli via pipx
RUN pipx install ctfcli

# ============================
#  Dependências Python dos plugins
# ============================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ============================
#  Plugins
# ============================
RUN rm -rf /opt/CTFd/CTFd/plugins
COPY --chown=1001:1001 plugins/ /opt/CTFd/CTFd/plugins/

# ============================
#  Temas
# ============================
RUN rm -rf /opt/CTFd/CTFd/themes
COPY --chown=1001:1001 themes/ /opt/CTFd/CTFd/themes/

# ============================
#  Permissões
# ============================
RUN chown -R 1001:1001 /opt/CTFd/CTFd/plugins /opt/CTFd/CTFd/themes /var/uploads

# ============================
#  Default
# ============================
WORKDIR /opt/CTFd
