import io
import os
import zipfile
from datetime import datetime
from pathlib import Path
from flask import Flask, jsonify, render_template, request, send_file

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{log_tamper_flag}")
LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_FILE = LOG_DIR / "audit.log"


def bootstrap():
    LOG_DIR.mkdir(exist_ok=True)
    if not LOG_FILE.exists():
        LOG_FILE.write_text(
            """2025-02-01 08:00:00;system;startup;engine online\n"
            "2025-02-01 08:10:12;audit;policy-check;no anomalies\n"
            f"2025-02-01 09:45:00;vault;flag;{FLAG}\n"
        )


def append_log(message: str):
    with LOG_FILE.open("a") as handle:
        handle.write(message + "\n")


bootstrap()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/api/logs")
def read_logs():
    content = LOG_FILE.read_text()
    return jsonify({"log": content.splitlines()[-20:]})


@app.route("/api/logs/write", methods=["POST"])
def write():
    body = request.get_json() or {}
    message = body.get("message")
    if not message:
        return jsonify({"error": "mensagem vazia"}), 400
    append_log(f"{datetime.utcnow().isoformat()}Z;{message}")
    return jsonify({"status": "ok"})


@app.route("/api/logs/export")
def export():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("audit.log", LOG_FILE.read_text())
    buffer.seek(0)
    return send_file(buffer, mimetype="application/zip", download_name="audit.zip", as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
