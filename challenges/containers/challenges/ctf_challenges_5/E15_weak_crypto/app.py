from flask import Flask, request, jsonify, render_template
import os
import base64
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{weak_crypto_modes}")
SECRET = b"itau-static-key"
KEY = md5(SECRET).digest()  # derivação fraca


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/token", methods=["POST"])
def token():
    data = request.json or {}
    user = data.get("user", "guest")
    payload = f"user={user};role=user"
    cipher = AES.new(KEY, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(payload.encode("utf-8"), AES.block_size))
    return jsonify({"token": base64.b64encode(encrypted).decode("utf-8"), "algo": "AES-ECB"})


@app.route("/flag")
def flag():
    token = request.headers.get("X-Session", "")
    if not token:
        return "no token", 403
    try:
        cipher = AES.new(KEY, AES.MODE_ECB)
        decrypted = unpad(cipher.decrypt(base64.b64decode(token)), AES.block_size)
        text = decrypted.decode("utf-8")
    except Exception:
        return "invalid token", 403
    if "role=admin" in text:
        return FLAG
    return "not enough privileges", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
