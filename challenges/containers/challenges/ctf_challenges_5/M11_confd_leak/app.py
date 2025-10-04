import os
from flask import Flask, jsonify, render_template

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{config_endpoint_leak}")
CONFIGS = {
    "dev": {"db": "postgres://dev"},
    "prod": {
        "db": "postgres://prod", 
        "secrets": {
            "flag": FLAG,
            "api_key": "prod-2025-secret"
        }
    }
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/api/config/<env>")
def config(env):
    data = CONFIGS.get(env)
    if not data:
        return jsonify({"error": "ambiente inválido"}), 404
    return jsonify({"env": env, "config": data})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
