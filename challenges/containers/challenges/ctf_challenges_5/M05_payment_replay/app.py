import os
from datetime import datetime
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{payment_replay_bonus}")
ledger = []
loyalty = {"cliente": 0}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/api/pay", methods=["POST"])
def pay():
    body = request.get_json() or {}
    reference = body.get("reference")
    amount = float(body.get("amount", 0))
    channel = body.get("channel", "app")

    if not reference or amount <= 0:
        return jsonify({"error": "Dados inválidos"}), 400

    entry = {
        "reference": reference,
        "amount": amount,
        "channel": channel,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    ledger.append(entry)
    loyalty["cliente"] += amount

    return jsonify({"status": "ok", "loyalty": loyalty["cliente"], "count": len(ledger)})


@app.route("/api/ledger")
def history():
    return jsonify({"ledger": ledger[-10:], "loyalty": loyalty["cliente"]})


@app.route("/flag")
def flag():
    if loyalty["cliente"] >= 5000:
        return FLAG
    return "Acumule mais pagamentos", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
