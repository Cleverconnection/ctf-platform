from flask import Flask, request, send_file, render_template, abort
import os
from pathlib import Path

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{file_download_traversal}")
BASE_DIR = Path("/app/files")
BASE_DIR.mkdir(exist_ok=True)
TOKEN_FILE = BASE_DIR / "flag_token.txt"
TOKEN_VALUE = "DOWNLOAD-KEY-2025"
if not TOKEN_FILE.exists():
    TOKEN_FILE.write_text(f"token={TOKEN_VALUE}\n", encoding="utf-8")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/download")
def download():
    target = request.args.get("path", "")
    if not target:
        abort(400)
    candidate = Path(os.path.join(str(BASE_DIR), target))
    file_path = candidate
    if not candidate.exists():
        file_path = Path(target)
    if not file_path.exists():
        abort(404)
    return send_file(file_path, as_attachment=True)


@app.route("/flag")
def flag():
    token = request.args.get("token", "")
    if token == TOKEN_VALUE:
        return FLAG
    return "forbidden", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
