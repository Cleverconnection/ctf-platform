from flask import Flask, request, render_template, send_file, abort
import os
from pathlib import Path

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{creds_in_query}")
BACKUP_DIR = Path("/app/backups")
BACKUP_DIR.mkdir(exist_ok=True)
BACKUP_TOKEN = "OPS-2025-SECRET"
BACKUP_FILE = BACKUP_DIR / "backup.enc"
if not BACKUP_FILE.exists():
    BACKUP_FILE.write_text("token=" + BACKUP_TOKEN + "\n", encoding="utf-8")


@app.route("/")
def index():
    return render_template("index.html", backup_token=BACKUP_TOKEN)


@app.route("/health")
def health():
    return "OK", 200


@app.route("/backup")
def backup():
    token = request.args.get("token")
    if token != BACKUP_TOKEN:
        abort(403)
    return send_file(BACKUP_FILE, as_attachment=True)


@app.route("/flag")
def flag():
    proof = request.args.get("token", "")
    if proof == BACKUP_TOKEN:
        return FLAG
    return "forbidden", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
