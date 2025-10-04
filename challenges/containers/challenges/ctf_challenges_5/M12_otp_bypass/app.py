import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{predictable_otp_bypass}")
ACCOUNT = "98765432100"


def calc_otp(identifier: str) -> str:
    seed = int(identifier[-6:])
    return f"{(seed * 3) % 1000000:06d}"


@app.route("/")
def index():
    return render_template("index.html", account=ACCOUNT)


@app.route("/health")
def health():
    return "OK", 200


@app.route("/api/send", methods=["POST"])
def send():
    data = request.get_json() or {}
    if data.get("account") != ACCOUNT:
        return jsonify({"error": "Conta desconhecida"}), 404
    otp = calc_otp(ACCOUNT)
    return jsonify({"status": "enviado", "hint": f"OTP termina com {otp[-2:]}"})


@app.route("/api/verify", methods=["POST"])
def verify():
    data = request.get_json() or {}
    account = data.get("account")
    otp = data.get("otp", "")

    if account != ACCOUNT:
        return jsonify({"error": "Conta inválida"}), 404

    if otp == calc_otp(account):
        return jsonify({"status": "ok", "flag": FLAG})

    return jsonify({"error": "OTP incorreto"}), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
