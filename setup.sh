#!/bin/bash
set -e

# raiz do projeto
mkdir -p ctf-infra
cd ctf-infra

# arquivos principais
touch docker-compose.yml
touch docker-compose.override.yml

# CTFd
mkdir -p ctfd/plugins/exemplo_plugin
mkdir -p ctfd/themes/exemplo_tema
touch ctfd/Dockerfile
touch ctfd/plugins/exemplo_plugin/__init__.py
touch ctfd/themes/exemplo_tema/README.md

# Spawner
mkdir -p spawner
cat > spawner/Dockerfile <<'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
EOF

cat > spawner/requirements.txt <<'EOF'
flask
docker
requests
EOF

cat > spawner/app.py <<'EOF'
from flask import Flask
app = Flask(__name__)

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
EOF

# Traefik
mkdir -p traefik/dynamic
touch traefik/traefik.yml
touch traefik/dynamic/middlewares.yml
touch traefik/dynamic/routers.yml

# Challenges
mkdir -p challenges/web-sqli/app
mkdir -p challenges/pwn-hello

cat > challenges/web-sqli/Dockerfile <<'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY app/ .
RUN pip install flask
CMD ["python", "app.py"]
EOF

cat > challenges/web-sqli/app/app.py <<'EOF'
from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Web SQLi challenge placeholder"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
EOF

echo "# Web SQLi Challenge" > challenges/web-sqli/README.md

cat > challenges/pwn-hello/Dockerfile <<'EOF'
FROM gcc:12
WORKDIR /chal
COPY chal.c .
RUN gcc -o chal chal.c -fno-stack-protector -no-pie
CMD ["./chal"]
EOF

cat > challenges/pwn-hello/chal.c <<'EOF'
#include <stdio.h>
#include <string.h>

int main() {
    char buf[64];
    printf("Welcome to pwn-hello! Enter something:\n");
    gets(buf); // Vulnerável
    printf("You entered: %s\n", buf);
    return 0;
}
EOF

# Data persistente
mkdir -p data/mysql data/redis data/uploads data/logs data/backups

echo "✅ Estrutura do CTF criada em $(pwd)"
