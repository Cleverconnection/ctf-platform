from flask import Flask, render_template, send_file, request
import os
from pathlib import Path
import zipfile

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{public_backup_flag}")
BACKUP_DIR = Path("/app/public")
BACKUP_DIR.mkdir(exist_ok=True)
ZIP_PATH = BACKUP_DIR / "backup.zip"
PROOF_CODE = "public-backup-2025"

if not ZIP_PATH.exists():
    flag_file = BACKUP_DIR / "flag.txt"
    flag_file.write_text(f"proof={PROOF_CODE}\nflag={FLAG}\n", encoding="utf-8")
    with zipfile.ZipFile(ZIP_PATH, "w") as archive:
        archive.write(flag_file, arcname="flag.txt")


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
    proof = request.args.get("proof", "")
    if proof == PROOF_CODE:
        return FLAG
    return "forbidden", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
