from flask import Flask, request, jsonify, render_template
import os
import jwt

app = Flask(__name__)
FLAG = "ITAU2025{jwt_without_expiration}"
JWT_SECRET = os.environ.get("JWT_SECRET", "supersecret")
ALGO = "HS256"


@app.route("/")
def index():
    return render_template("index.html", algo=ALGO)


@app.route("/health")
def health():
    return "OK", 200


@app.route("/token", methods=["POST"])
def token():
    data = request.json or {}
    user = data.get("user", "guest")
    payload = {"sub": user, "role": "user"}
    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGO)
    if isinstance(token, bytes):
        token = token.decode()
    return jsonify({"token": token, "payload": payload})


@app.route("/flag")
def flag():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return "no auth", 403
    token = auth.split(None, 1)[1]
    try:
        decoded = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[ALGO],
            options={"verify_exp": False},
        )
    except Exception:
        return "invalid token", 403
    if decoded.get("role") == "admin":
        return FLAG
    return "not enough privileges", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
