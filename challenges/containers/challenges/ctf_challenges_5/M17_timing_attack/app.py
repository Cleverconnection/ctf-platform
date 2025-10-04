import os
import time
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{timing_leak_username}")
USERS = {"executivo": "9246"}
DELAY = 0.12


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


def compare_slow(a: str, b: str) -> bool:
    for x, y in zip(a, b):
        if x != y:
            return False
        time.sleep(DELAY)
    return len(a) == len(b)


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username", "")
    password = data.get("password", "")

    stored = USERS.get(username)
    if stored is None:
        time.sleep(0.02)
        return jsonify({"error": "credenciais inválidas"}), 401

    if compare_slow(password, stored):
        return jsonify({"status": "ok", "flag": FLAG})

    return jsonify({"error": "credenciais inválidas"}), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
