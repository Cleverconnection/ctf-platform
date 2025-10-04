from flask import Flask, request, jsonify, render_template, make_response
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{tls_redirect_missing}")
SESSION_VALUE = "E18-SESSION-2025"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/session")
def session_view():
    proto = request.headers.get("X-Forwarded-Proto", request.scheme)
    resp = make_response(jsonify({
        "message": "Sessão criada",
        "protocol": proto,
        "session": SESSION_VALUE,
    }))
    resp.set_cookie("session", SESSION_VALUE)
    return resp


@app.route("/flag")
def flag():
    session = request.args.get("session", "")
    if session == SESSION_VALUE:
        return FLAG
    return "forbidden", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
