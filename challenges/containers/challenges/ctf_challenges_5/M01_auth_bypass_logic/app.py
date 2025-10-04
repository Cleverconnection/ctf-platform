import os
import secrets
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{auth_logic_mfa_bypass}")
USERS = {"analyst": "senh@F0rte"}
MFA_CODES = {"analyst": "314159"}
sessions = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/api/start", methods=["POST"])
def start_login():
    data = request.get_json() or {}
    username = data.get("username", "")
    password = data.get("password", "")

    if USERS.get(username) == password:
        session_id = secrets.token_hex(8)
        sessions[session_id] = {"user": username, "step": "password_ok"}
        return jsonify({
            "session_id": session_id,
            "next": "mfa",
            "message": "Senha validada. Informe o token MFA."
        })

    return jsonify({"error": "Credenciais inválidas"}), 401


@app.route("/api/mfa", methods=["POST"])
def validate_mfa():
    data = request.get_json() or {}
    session_id = data.get("session_id")
    code = data.get("code", "")
    state = sessions.get(session_id)

    if not state:
        return jsonify({"error": "Sessão inválida"}), 400

    user = state["user"]
    expected = MFA_CODES.get(user)

    if expected and code == expected:
        sessions[session_id]["step"] = "mfa_ok"
        return jsonify({"status": "ok", "next": "complete"})

    return jsonify({"error": "Token incorreto"}), 401


@app.route("/api/complete", methods=["POST"])
def finalize_login():
    data = request.get_json() or {}
    session_id = data.get("session_id")
    claimed_step = data.get("step", "")
    state = sessions.get(session_id)

    if not state:
        return jsonify({"error": "Sessão inválida"}), 400

    if claimed_step == "mfa_ok":
        return jsonify({"status": "admin", "flag": FLAG})

    return jsonify({"error": "Fluxo incompleto"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
