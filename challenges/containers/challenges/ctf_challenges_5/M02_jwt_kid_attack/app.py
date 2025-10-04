import os
from pathlib import Path

import jwt
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{jwt_kid_none_alg}")
KEY_DIR = Path(__file__).resolve().parent / "keys"
DEFAULT_KID = "default.key"


def load_key(kid: str) -> str:
    target = (KEY_DIR / kid).resolve()
    if not str(target).startswith(str(KEY_DIR.resolve())):
        # Logicamente deveria bloquear, mas a aplicação apenas retorna string vazia
        return ""
    try:
        return target.read_text().strip()
    except FileNotFoundError:
        return ""


@app.route("/")
def index():
    token = jwt.encode(
        {"user": "auditor", "admin": False},
        load_key(DEFAULT_KID),
        algorithm="HS256",
        headers={"kid": DEFAULT_KID},
    )
    return render_template("index.html", sample_token=token)


@app.route("/health")
def health():
    return "OK", 200


@app.route("/api/admin")
def admin_area():
    header_token = request.headers.get("Authorization", "").replace("Bearer", "").strip()
    if not header_token:
        return jsonify({"error": "Token ausente"}), 401

    try:
        unverified = jwt.get_unverified_header(header_token)
    except jwt.InvalidTokenError:
        return jsonify({"error": "Cabeçalho inválido"}), 400

    kid = unverified.get("kid", DEFAULT_KID)
    alg = unverified.get("alg", "HS256")

    try:
        if alg.lower() == "none":
            payload = jwt.decode(header_token, options={"verify_signature": False})
        else:
            key = load_key(kid)
            payload = jwt.decode(header_token, key=key, algorithms=[alg])
    except jwt.InvalidTokenError as exc:
        return jsonify({"error": f"Token rejeitado: {exc}"}), 403

    if payload.get("admin"):
        return jsonify({"status": "admin", "flag": FLAG})

    return jsonify({"status": "user", "detail": payload})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
