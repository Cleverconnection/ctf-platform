from flask import Flask, request, jsonify, render_template
import secrets

app = Flask(__name__)
FLAG = "ITAU2025{weak_passwords_ruin_security}"

USERS = {
    "admin": "admin123",  # intentionally weak
    "service": "Password1",
}
TOKENS = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    user = data.get("user", "")
    pwd = data.get("password", "")
    if user in USERS and USERS[user] == pwd:
        token = secrets.token_hex(16)
        TOKENS[token] = user
        return jsonify({"token": token})
    return jsonify({"error": "invalid credentials"}), 403


@app.route("/flag")
def flag():
    token = request.args.get("token", "")
    if token in TOKENS:
        return FLAG
    return "forbidden", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
