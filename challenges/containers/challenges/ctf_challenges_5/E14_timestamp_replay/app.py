from flask import Flask, request, jsonify, render_template
import os
from datetime import datetime, timezone
from collections import defaultdict

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{timestamp_replay_attack}")
BALANCES = defaultdict(int)
TOKEN_THRESHOLD = 1000
FLAG_TOKEN = "REPLAY-2025-CODE"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/transfer", methods=["POST"])
def transfer():
    data = request.json or {}
    account = data.get("account", "")
    amount = int(data.get("amount", 0))
    timestamp = data.get("timestamp")
    if not account or not timestamp:
        return jsonify({"error": "payload incompleto"}), 400
    if amount <= 0 or amount > 100:
        return jsonify({"error": "valor inválido"}), 400
    try:
        sent_at = datetime.fromisoformat(timestamp)
    except Exception:
        return jsonify({"error": "timestamp inválido"}), 400
    now = datetime.now(timezone.utc)
    if abs((now - sent_at).total_seconds()) > 600:
        return jsonify({"error": "timestamp fora da janela"}), 400
    BALANCES[account] += amount
    response = {"status": "processado", "credited": amount, "account": account}
    if BALANCES[account] >= TOKEN_THRESHOLD:
        response["flag_token"] = FLAG_TOKEN
    return jsonify(response)


@app.route("/flag")
def flag():
    token = request.args.get("token", "")
    if token == FLAG_TOKEN:
        return FLAG
    return "forbidden", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
