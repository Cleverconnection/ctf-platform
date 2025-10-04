import os
import subprocess
from pathlib import Path

from flask import Flask, render_template, request, send_file

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{public_backup_flag}")
BACKUP_DIR = Path("/app/public")
BACKUP_DIR.mkdir(exist_ok=True)
ZIP_PATH = BACKUP_DIR / "backup.zip"
ZIP_PASSWORD = "restore-2025"
PLAINTEXT_FLAG = BACKUP_DIR / "flag.txt"
PROOF_CODE = "public-backup-2025"

if not ZIP_PATH.exists():
    PLAINTEXT_FLAG.write_text(f"proof={PROOF_CODE}\nflag={FLAG}\n", encoding="utf-8")
    subprocess.run(
        ["zip", "-j", "-P", ZIP_PASSWORD, str(ZIP_PATH), str(PLAINTEXT_FLAG)],
        check=True,
        capture_output=True,
    )
    PLAINTEXT_FLAG.unlink(missing_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/backup.zip")
def download():
    return send_file(ZIP_PATH, as_attachment=True)


@app.route("/flag")
def flag():
    return "flag disponível apenas dentro do backup protegido", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
