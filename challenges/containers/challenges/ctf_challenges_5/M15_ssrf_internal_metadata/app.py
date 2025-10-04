import os
from urllib.parse import urlparse

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{metadata_ssrf_flag}")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/api/report")
def report():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "url ausente"}), 400

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return jsonify({"error": "apenas http(s)"}), 400

    try:
        resp = requests.get(url, timeout=2)
        return jsonify({"status": resp.status_code, "body": resp.text[:2000]})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 502


@app.route("/metadata/iam")
def metadata():
    if request.remote_addr not in {"127.0.0.1", "::1"}:
        return "denied", 403
    return jsonify({
        "Code": "Success",
        "LastUpdated": "2025-02-01T10:00:00Z",
        "AccessKeyId": "AKIA-INTERNAL",
        "SecretAccessKey": FLAG,
        "Token": "session-token",
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
