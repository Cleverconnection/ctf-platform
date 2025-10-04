from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{rate_limit_bypass}")
SECRET_OTP = "7391"
FLAG_TOKEN = "RATE-LIMIT-2025"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/otp", methods=["POST"])
def otp():
    data = request.json or {}
    code = data.get("code", "")
    if code == SECRET_OTP:
        return jsonify({"status": "ok", "flag_token": FLAG_TOKEN})
    return jsonify({"status": "fail"}), 401


@app.route("/flag")
def flag():
    token = request.args.get("token", "")
    if token == FLAG_TOKEN:
        return FLAG
    return "forbidden", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
