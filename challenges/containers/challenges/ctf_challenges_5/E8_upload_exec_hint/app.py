from flask import Flask, request, render_template, jsonify, send_from_directory
import os
from pathlib import Path
from werkzeug.utils import secure_filename

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{predictable_upload_leak}")
UPLOAD_DIR = Path("/app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
FLAG_NOTE = UPLOAD_DIR / "relatorio_flag.txt"
ACCESS_KEY = "SHIFT-UPLOAD-2025"

if not FLAG_NOTE.exists():
    FLAG_NOTE.write_text(
        "Relatório confidencial\nChave de liberação: " + ACCESS_KEY + "\n",
        encoding="utf-8",
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/upload", methods=["POST"])
def upload():
    uploaded = request.files.get("file")
    if not uploaded:
        return jsonify({"error": "arquivo ausente"}), 400
    filename = secure_filename(uploaded.filename) or "arquivo.txt"
    predictable = filename.lower().replace(" ", "_")
    save_path = UPLOAD_DIR / predictable
    uploaded.save(save_path)
    return jsonify({"saved_as": predictable, "url": f"/files/{predictable}"})


@app.route("/files/<path:name>")
def files(name: str):
    return send_from_directory(UPLOAD_DIR, name, as_attachment=False)


@app.route("/flag")
def flag():
    key = request.args.get("key", "")
    if key == ACCESS_KEY:
        return FLAG
    return "forbidden", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
