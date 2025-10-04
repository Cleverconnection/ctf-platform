import os
from flask import Flask, jsonify, make_response, render_template, request

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{csrf_cookie_api}")
transfers = []


@app.after_request
def apply_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Credentials"] = "true"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return resp


@app.route("/", methods=["GET"])
def index():
    resp = make_response(render_template("index.html"))
    resp.set_cookie("session", "analyst", httponly=False, samesite="None")
    return resp


@app.route("/health")
def health():
    return "OK", 200


@app.route("/api/profile")
def profile():
    if request.cookies.get("session") != "analyst":
        return jsonify({"error": "não autenticado"}), 401
    return jsonify({"user": "analyst", "limits": 1500})


@app.route("/api/transfer", methods=["POST", "OPTIONS"])
def transfer():
    if request.method == "OPTIONS":
        return ("", 204)

    if request.cookies.get("session") != "analyst":
        return jsonify({"error": "não autenticado"}), 401

    body = request.get_json() or {}
    transfers.append(body)

    if body.get("to") == "shadow" and int(body.get("amount", 0)) >= 1200:
        return jsonify({"status": "ok", "flag": FLAG})

    return jsonify({"status": "ok", "detail": body})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
