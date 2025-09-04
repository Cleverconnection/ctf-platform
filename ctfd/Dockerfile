# Imagem base estável do CTFd
FROM ghcr.io/ctfd/ctfd:3.7.7

# Rodar passos de build como root
USER root

# Instalar dependências Python no venv do CTFd (necessário p/ plugin containers)
# Fixamos a versão p/ reprodutibilidade
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ============================
#  Plugins
# ============================
# Copiamos explicitamente os plugins que você quer usar.
# OBS: Se você NÃO alterou o plugin "containers", pode omitir este COPY —
# o plugin já existe na imagem base. Mantenho aqui caso você queira sobrepor ajustes.
#COPY plugins/containers/   /opt/CTFd/CTFd/plugins/containers/
#COPY plugins/team_notes/   /opt/CTFd/CTFd/plugins/team_notes/
RUN rm -rf /opt/CTFd/CTFd/plugins
#COPY plugins/              /opt/CTFd/CTFd/plugins/
COPY --chown=1001:1001 plugins/ /opt/CTFd/CTFd/plugins/

# ============================
#  Temas (SUBSTITUIR diretório completo)
# ============================
# ATENÇÃO: seu diretório "themes/" DEVE conter core/ e admin/
# Caso contrário, a UI/Admin do CTFd vai quebrar.
RUN rm -rf /opt/CTFd/CTFd/themes
#COPY themes/               /opt/CTFd/CTFd/themes/
COPY --chown=1001:1001 themes/  /opt/CTFd/CTFd/themes/

# Permissões para o usuário padrão da imagem (uid/gid 1001)
RUN chown -R 1001:1001 /opt/CTFd/CTFd/plugins /opt/CTFd/CTFd/themes /var/uploads

# Volta para o usuário não-root padrão
#USER 1001
WORKDIR /opt/CTFd
# ENTRYPOINT/CMD permanecem os da imagem base
