FROM debian:bookworm-slim

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# -------- Pacotes necessários --------
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    gcc make libc6-dev ca-certificates \
    openssh-server bash coreutils findutils file strace ltrace procps \
 && rm -rf /var/lib/apt/lists/*

# -------- Constantes --------
ENV CHALLENGE_DIR="/challenge/app-script/ch11" \
    OWNER_CRACKED="app-script-ch11-cracked" \
    GROUP="app-script-ch11" \
    BIN="ch11" \
    FLAG="FLAG{A3E1D7F2C9B4058E7A2D16C3F0B94E6D}"

# -------- Usuários/Grupos --------
RUN groupadd -r "${GROUP}" \
 && useradd -r -s /usr/sbin/nologin "${OWNER_CRACKED}" \
 && useradd -m -s /bin/bash player \
 && usermod -a -G "${GROUP}" player \
 && echo 'player:player' | chpasswd   # senha do usuário para SSH

# -------- Código-fonte --------
WORKDIR /opt/build
RUN mkdir -p levels dist

RUN cat > levels/ch11v4.c <<'EOF'
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main(void) {
    setreuid(geteuid(), geteuid());
    // mitigação do PATH hijack básico: caminho absoluto
    system("/bin/ls /challenge/app-script/ch11/.passwd");
    return 0;
}
EOF

RUN gcc -Wall -Wextra -O2 -s -o dist/ch11v4 levels/ch11v4.c

# -------- Instala desafio --------
RUN set -euo pipefail; \
    install -d -m 0550 "${CHALLENGE_DIR}"; \
    chown "${OWNER_CRACKED}:${GROUP}" "${CHALLENGE_DIR}"; \
    install -m 0550 dist/ch11v4 "${CHALLENGE_DIR}/${BIN}"; \
    printf '%s\n' "${FLAG}" > "${CHALLENGE_DIR}/.passwd"; \
    printf "bin=%s\nlevel=v4\n" "${BIN}" > "${CHALLENGE_DIR}/._perms"; \
    chown "${OWNER_CRACKED}:${GROUP}" "${CHALLENGE_DIR}/${BIN}" "${CHALLENGE_DIR}/.passwd"; \
    chown root:root "${CHALLENGE_DIR}/._perms"; \
    chmod u+s "${CHALLENGE_DIR}/${BIN}"; \
    chmod 0400 "${CHALLENGE_DIR}/.passwd"; \
    chmod 0440 "${CHALLENGE_DIR}/._perms"; \
    rm -rf /opt/build

# -------- Configura SSH --------
RUN mkdir /var/run/sshd \
 && sed -i 's/^#Port 22/Port 2222/' /etc/ssh/sshd_config \
 && sed -i 's/^#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config \
 && sed -i 's/^UsePAM yes/UsePAM no/' /etc/ssh/sshd_config

# -------- Mensagem MOTD --------
RUN cat > /etc/motd <<'EOF'
========================================
App Script — System 1 (v4)
- Acesse via SSH: porta 2222
- Usuário: player | Senha: player
- Binário SUID: /challenge/app-script/ch11/ch11
- Objetivo: ler o conteúdo de .passwd
========================================
EOF

EXPOSE 2222

CMD ["/usr/sbin/sshd", "-D"]
