from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{swagger_spill}")
ADMIN_KEY = "E10-ADMIN-KEY-2025"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/swagger.json")
def swagger():
    spec = {
        "openapi": "3.0.1",
        "info": {
            "title": "Itaú Internal Ops",
            "version": "1.0.0",
            "description": "Spec interno para integrações de suporte."
        },
        "paths": {
            "/api/internal/login": {
                "post": {
                    "summary": "Autentica operadores",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "api_key": {"type": "string", "example": ADMIN_KEY}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Sessão criada"}
                    }
                }
            }
        }
    }
    return jsonify(spec)


@app.route("/api/internal/login", methods=["POST"])
def internal_login():
    body = request.json or {}
    if body.get("api_key") == ADMIN_KEY:
        return jsonify({"status": "ok", "flag_endpoint": "/flag"})
    return jsonify({"error": "credenciais inválidas"}), 403


@app.route("/flag")
def flag():
    key = request.headers.get("X-API-Key", "")
    if key == ADMIN_KEY:
        return FLAG
    return "forbidden", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
