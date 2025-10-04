import os
from pathlib import Path
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{object_storage_flag}")
BASE_DIR = Path(__file__).resolve().parent / "storage"


def sync_flag():
    secret = BASE_DIR / "private"
    secret.mkdir(parents=True, exist_ok=True)
    (secret / "flag.txt").write_text(FLAG)


sync_flag()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/api/file")
def serve_file():
    name = request.args.get("path")
    if not name:
        return jsonify({"error": "path ausente"}), 400

    path = BASE_DIR / name
    try:
        content = path.read_text()
        return jsonify({"path": name, "content": content})
    except FileNotFoundError:
        return jsonify({"error": "arquivo não encontrado"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
