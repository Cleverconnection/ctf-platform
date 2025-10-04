import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{auth_header_split}")
VALID_TOKEN = "svc-ops-2025"


@app.route("/")
def index():
    return render_template("index.html", token=VALID_TOKEN)


@app.route("/health")
def health():
    return "OK", 200


@app.route("/api/secure")
def secure():
    header = request.headers.get("Authorization", "")
    if not header.startswith("Token "):
        return jsonify({"error": "header ausente"}), 401

    fields = {}
    for part in header[6:].split(";"):
        if "=" in part:
            key, value = part.split("=", 1)
            fields[key.strip().lower()] = value.strip()

    if fields.get("token") != VALID_TOKEN:
        return jsonify({"error": "token inválido", "parsed": fields}), 403

    role = fields.get("role", "analyst")
    if role == "admin":
        return jsonify({"status": "ok", "flag": FLAG, "role": role})

    return jsonify({"status": "ok", "role": role})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
