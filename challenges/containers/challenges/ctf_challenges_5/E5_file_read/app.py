import os
import secrets
from datetime import datetime, timedelta

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
FLAG = "ITAU2025{path_traversal_master}"
APP_ROOT = "/app/data"
TOKENS: dict[str, datetime] = {}
TOKEN_TTL = timedelta(minutes=5)


def _issue_token() -> tuple[str, int]:
    token = secrets.token_urlsafe(16)
    expires_at = datetime.utcnow() + TOKEN_TTL
    TOKENS[token] = expires_at
    return token, int(TOKEN_TTL.total_seconds())


def _consume_token(value: str) -> bool:
    expires_at = TOKENS.pop(value, None)
    if not expires_at:
        return False
    if expires_at < datetime.utcnow():
        return False
    return True


@app.route("/")
def index():
    files = []
    try:
        files = sorted(os.listdir(APP_ROOT))
    except FileNotFoundError:
        pass
    return render_template("index.html", files=files)


@app.route("/health")
def health():
    return "OK", 200


@app.route("/read")
def read():
    fname = request.args.get("file", "")
    if not fname:
        return "specify ?file="
    target = os.path.join(APP_ROOT, fname)
    try:
        with open(target, "rb") as handle:
            return handle.read(), 200
    except Exception as exc:
        return f"error: {exc}", 404


@app.route("/handshake", methods=["POST"])
def handshake():
    payload = request.get_json(silent=True) or {}
    if payload.get("aceite") != "sim":
        return jsonify({"error": "confirme o aceite das condições para gerar o token."}), 400
    token, ttl = _issue_token()
    return jsonify({"token": token, "expires_in": ttl})


@app.route("/flag", methods=["GET", "POST"])
def flag():
    if request.method == "GET":
        return "fluxo protegido: envie POST com token válido", 403

    payload = request.get_json(silent=True) or {}
    token = payload.get("token", "").strip()
    if not token:
        return jsonify({"error": "token obrigatório"}), 400

    if not _consume_token(token):
        return jsonify({"error": "token inválido ou expirado"}), 403

    return jsonify({"flag": FLAG})


if __name__ == "__main__":
    os.makedirs(APP_ROOT, exist_ok=True)
    with open(os.path.join(APP_ROOT, "public.txt"), "w", encoding="utf-8") as handle:
        handle.write("public info\n")
    app.run(host="0.0.0.0", port=8080)
