from flask import Flask, request, render_template, send_file, abort, redirect
import os
from pathlib import Path

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{creds_in_query}")
BACKUP_DIR = Path("/app/backups")
BACKUP_DIR.mkdir(exist_ok=True)
BACKUP_TOKEN = "OPS-2025-SECRET"
BACKUP_FILE = BACKUP_DIR / "backup.enc"
REDIRECT_MAP = {"backup": f"/backup?token={BACKUP_TOKEN}"}
if not BACKUP_FILE.exists():
    BACKUP_FILE.write_text("token=" + BACKUP_TOKEN + "\n", encoding="utf-8")


@app.route("/")
def index():
    return render_template("index.html", redirect_id="backup")


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


@app.route("/r/<link_id>")
def redirect_link(link_id: str):
    target = REDIRECT_MAP.get(link_id)
    if not target:
        abort(404)
    app.logger.info("redirect %s from %s", link_id, request.remote_addr)
    return redirect(target, code=302)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
