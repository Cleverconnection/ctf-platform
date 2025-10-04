FROM ahgcontato/arena
# Copia configuração de CTF (ativa flags nos toasts)
COPY config/ctf.yml /juice-shop/config/ctf.yml

# Copia lista de challenges (apenas os 5 que você quer)
COPY data/static/challenges.yml /juice-shop/data/static/challenges.yml

# Remove o SQLite para forçar resemeadura só com esses challenges
RUN rm -f /juice-shop/data/juiceshop.sqlite

# Expõe a porta padrão
EXPOSE 3000

# Garante que suba em modo CTF
ENV NODE_ENV=ctf
#ENV CTF_KEY=seu-segredo-aqui

CMD ["npm", "start"]
