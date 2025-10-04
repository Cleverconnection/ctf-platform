import os
import time
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{race_condition_transfer}")
accounts = {
    "pagamentos": {"owner": "Tesouraria", "balance": 3000},
    "cobrancas": {"owner": "Cobrança", "balance": 2800},
    "fraude": {"owner": "Conta Teste", "balance": 200},
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/api/state")
def state():
    return jsonify(accounts)


@app.route("/api/transfer", methods=["POST"])
def transfer():
    data = request.get_json() or {}
    src = data.get("from")
    dst = data.get("to")
    amount = int(data.get("amount", 0))

    if src not in accounts or dst not in accounts:
        return jsonify({"error": "Conta inválida"}), 400

    if amount <= 0:
        return jsonify({"error": "Valor inválido"}), 400

    src_acc = accounts[src]
    dst_acc = accounts[dst]

    if src_acc["balance"] < amount:
        return jsonify({"error": "Saldo insuficiente"}), 409

    time.sleep(0.7)
    src_acc["balance"] -= amount
    dst_acc["balance"] += amount

    return jsonify({"status": "ok", "balances": accounts})


@app.route("/flag")
def flag():
    if accounts["fraude"]["balance"] >= 4000:
        return FLAG
    return "Conclua o desvio primeiro", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
