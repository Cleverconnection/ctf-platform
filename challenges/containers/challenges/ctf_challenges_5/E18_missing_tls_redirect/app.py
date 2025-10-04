import os
import secrets
from datetime import datetime, timedelta

from flask import Flask, jsonify, make_response, render_template, request

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{tls_redirect_missing}")
SESSION_VALUE = "E18-SESSION-2025"
BOARDING_TICKET = "BOARDING-2025"
TOKEN_TTL = timedelta(minutes=5)
ACTIVE_HANDSHAKES: dict[str, datetime] = {}


def _require_https() -> bool:
    proto = request.headers.get("X-Forwarded-Proto", request.scheme)
    return proto == "https"


def _issue_handshake() -> tuple[str, int]:
    token = secrets.token_urlsafe(16)
    ACTIVE_HANDSHAKES[token] = datetime.utcnow() + TOKEN_TTL
    return token, int(TOKEN_TTL.total_seconds())


def _consume_handshake(value: str) -> bool:
    expires = ACTIVE_HANDSHAKES.pop(value, None)
    if not expires:
        return False
    if expires < datetime.utcnow():
        return False
    return True


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/login", methods=["POST"])
def login():
    if not _require_https():
        return jsonify({"error": "conexão insegura detectada"}), 403

    payload = request.get_json(silent=True) or {}
    if payload.get("ticket") != BOARDING_TICKET:
        return jsonify({"error": "bilhete inválido"}), 403

    token, ttl = _issue_handshake()
    return jsonify({"handshake_token": token, "expires_in": ttl})


@app.route("/session")
def session_view():
    proto = request.headers.get("X-Forwarded-Proto", request.scheme)
    transit_token = request.headers.get("X-Transit-Token") or request.args.get("handshake", "")
    if not transit_token or not _consume_handshake(transit_token):
        return jsonify({"error": "handshake obrigatório"}), 403

    resp = make_response(
        jsonify({
            "message": "Sessão criada",
            "protocol": proto,
            "session": SESSION_VALUE,
        })
    )
    resp.set_cookie("session", SESSION_VALUE, httponly=True, samesite="Lax")
    return resp


@app.route("/flag")
def flag():
    session = request.args.get("session", "")
    if session == SESSION_VALUE:
        return FLAG
    return "forbidden", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
