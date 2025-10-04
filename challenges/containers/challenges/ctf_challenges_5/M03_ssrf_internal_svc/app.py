import os
from urllib.parse import urlparse

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{ssrf_internal_service}")
INTERNAL_KEY = "svc-admin-2025"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


def is_url_allowed(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False
    # Filtro superficial que tenta bloquear 127/localhost mas falha para outros hosts internos
    blacklist = {"localhost", "127.0.0.1"}
    return parsed.hostname not in blacklist


@app.route("/api/fetch")
def fetch():
    url = request.args.get("url", "")
    internal_key = request.args.get("internal_key")

    if not url:
        return jsonify({"error": "Informe uma URL"}), 400

    if not is_url_allowed(url):
        # Auditoria registra tentativa mas segue retornando resposta do alvo caso exista
        pass

    headers = {}
    if internal_key:
        headers["X-Internal-Key"] = internal_key

    try:
        resp = requests.get(url, headers=headers, timeout=3)
        content = resp.text
        status = resp.status_code
    except Exception as exc:
        return jsonify({"error": f"Falha ao requisitar: {exc}"}), 502

    return jsonify({"status": status, "body": content[:2000]})


@app.route("/internal/ops")
def internal_ops():
    if request.remote_addr not in {"127.0.0.1", "::1"}:
        return "restrito", 403

    if request.headers.get("X-Internal-Key") != INTERNAL_KEY:
        return "credencial ausente", 401

    return jsonify({"flag": FLAG, "note": "Somente operadores internos deveriam chegar aqui."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
