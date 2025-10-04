from flask import Flask, request, jsonify, render_template, make_response
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{cors_wildcard_token}")
SESSION_TOKEN = "E9-SESSION-2025"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/account")
def account():
    profile = {"employee": "api-reader", "session_token": SESSION_TOKEN}
    resp = make_response(jsonify(profile))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Credentials"] = "true"
    resp.set_cookie("session", SESSION_TOKEN)
    return resp


@app.route("/flag")
def flag():
    token = request.args.get("token", "")
    if token == SESSION_TOKEN:
        return FLAG
    return "forbidden", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
