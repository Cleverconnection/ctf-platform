import os

from flask import Flask, jsonify, make_response, render_template, request

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{cors_wildcard_token}")
SESSION_TOKEN = "E9-SESSION-2025"
PROGRESS_TOKEN = "E9-PROGRESS-ALPHA"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/account")
def account():
    profile = {
        "employee": "api-reader",
        "permissoes": ["relatorios:ler"],
        "status": "sessao parcial emitida",
    }
    resp = make_response(jsonify(profile))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Credentials"] = "true"
    resp.headers["Access-Control-Expose-Headers"] = "X-Progress-Token"
    resp.headers["X-Progress-Token"] = PROGRESS_TOKEN
    resp.set_cookie("session", SESSION_TOKEN, httponly=True, samesite="None")
    return resp


@app.route("/internal/session")
def internal_session():
    provided = request.headers.get("X-Progress-Token") or request.args.get("progress_token", "")
    if provided != PROGRESS_TOKEN:
        return jsonify({"error": "token inválido para troca interna"}), 403

    resp = make_response(
        jsonify({
            "session_token": SESSION_TOKEN,
            "note": "Uso exclusivo do backend interno para promover a sessão completa.",
        })
    )
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Credentials"] = "true"
    return resp


@app.route("/flag")
def flag():
    token = request.args.get("token", "") or request.cookies.get("session", "")
    if token == SESSION_TOKEN:
        return FLAG
    return "acesso negado", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
