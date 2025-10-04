import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{api_privilege_escalation}")
user = {
    "username": "analyst",
    "role": {"name": "analyst", "canApprove": False},
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/api/users/me")
def me():
    return jsonify(user)


@app.route("/api/users/me", methods=["PATCH"])
def update():
    body = request.get_json() or {}
    role_patch = body.get("role")

    if isinstance(role_patch, dict):
        if "canApprove" in role_patch:
            user_role = user.setdefault("role", {})
            user_role["canApprove"] = bool(role_patch["canApprove"])
        if "name" in role_patch:
            desired = str(role_patch["name"])
            if desired.startswith("branch-"):
                user.setdefault("role", {})["name"] = desired
    elif isinstance(role_patch, str):
        # Suporte legado converte a role para string diretamente
        user["role"] = role_patch

    return jsonify({"status": "ok", "role": user["role"]})


@app.route("/flag")
def flag():
    role = user.get("role")
    if isinstance(role, dict) and role.get("name") == "admin":
        return FLAG
    if isinstance(role, str) and role.lower() == "admin":
        return FLAG
    return "Somente administradores podem ver", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
