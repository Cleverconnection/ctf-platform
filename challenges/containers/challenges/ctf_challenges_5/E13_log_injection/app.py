from flask import Flask, request, render_template, jsonify
import os
from pathlib import Path

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{logs_are_trust_issue}")
LOG_FILE = Path("/app/audit.log")
LOG_FILE.touch(exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/report", methods=["POST"])
def report():
    payload = request.json or {}
    message = payload.get("message", "")
    entry = f"{request.remote_addr} | {message}\n"
    with LOG_FILE.open("a", encoding="utf-8") as handler:
        handler.write(entry)
    return jsonify({"logged": entry.strip()})


@app.route("/logs")
def logs():
    return LOG_FILE.read_text(encoding="utf-8")


@app.route("/flag")
def flag():
    token = request.args.get("token", "")
    log_content = LOG_FILE.read_text(encoding="utf-8")
    if f"FLAG_TOKEN={token}" in log_content:
        return FLAG
    return "forbidden", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
