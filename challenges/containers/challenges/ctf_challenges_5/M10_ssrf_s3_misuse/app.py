import os
from urllib.parse import urlparse

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{ssrf_s3_traversal}")
INTERNAL_BUCKET = "internal-audit"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/info")
def info():
    return render_template("info.html", bucket=INTERNAL_BUCKET)


@app.route("/health")
def health():
    return "OK", 200


@app.route("/api/proxy")
def proxy():
    target = request.args.get("url")
    if not target:
        return jsonify({"error": "Informe url"}), 400

    parsed = urlparse(target)
    if parsed.scheme not in {"http", "https"}:
        return jsonify({"error": "Somente http/https"}), 400

    headers = {}
    if request.args.get("forward_headers", "true") == "true":
        headers["User-Agent"] = "workflow-proxy/1.0"

    try:
        resp = requests.get(target, headers=headers, timeout=3)
        return jsonify({"status": resp.status_code, "body": resp.text[:2000]})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 502


@app.route("/s3/internal/<path:key>")
def s3_internal(key):
    if request.remote_addr not in {"127.0.0.1", "::1"}:
        return "forbidden", 403

    if key == "statements/report.txt":
        return f"bucket:{INTERNAL_BUCKET}\nreport:Q4\nflag:{FLAG}\n"

    return "no such key", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
