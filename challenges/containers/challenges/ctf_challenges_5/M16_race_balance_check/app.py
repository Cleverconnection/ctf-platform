import os
import time
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{race_negative_balance}")
state = {"checking": 1500, "credit": 500}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/api/state")
def status():
    return jsonify(state)


@app.route("/api/withdraw", methods=["POST"])
def withdraw():
    body = request.get_json() or {}
    amount = int(body.get("amount", 0))

    if amount <= 0:
        return jsonify({"error": "valor inválido"}), 400

    current = state["checking"]
    if current < amount:
        return jsonify({"error": "saldo insuficiente", "balance": current}), 409

    time.sleep(0.6)
    state["checking"] -= amount
    return jsonify({"status": "ok", "balance": state["checking"]})


@app.route("/flag")
def flag():
    if state["checking"] < 0:
        return FLAG
    return "Balance não negativo", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
