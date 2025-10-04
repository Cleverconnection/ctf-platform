from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{reset_enum_abuse}")
USERS = {
    "1001": {"email": "cliente@itau.com", "reset": "https://reset.itau/reset?token=USER-1001"},
    "4010": {"email": "suporte@itau.com", "reset": "https://reset.itau/reset?token=USER-4010"},
    "9001": {"email": "ceo@itau.com", "reset": "https://reset.itau/reset?token=RESET-2025-ADMIN"},
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/forgot")
def forgot():
    user_id = request.args.get("id", "")
    user = USERS.get(user_id)
    if not user:
        return jsonify({"error": "usuário não encontrado"}), 404
    return jsonify({"email": user["email"], "reset_link": user["reset"]})


@app.route("/flag")
def flag():
    token = request.args.get("token", "")
    if token == "RESET-2025-ADMIN":
        return FLAG
    return "forbidden", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
