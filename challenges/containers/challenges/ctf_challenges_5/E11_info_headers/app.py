from flask import Flask, render_template, request, jsonify, make_response, send_file
import os
from pathlib import Path

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{headers_tell_secrets}")
INTERNAL_PATH = Path("/srv/bank/flag_hint.txt")
INTERNAL_PATH.parent.mkdir(parents=True, exist_ok=True)
HINT_VALUE = "E11-HINT-2025"
if not INTERNAL_PATH.exists():
    INTERNAL_PATH.write_text(f"hint={HINT_VALUE}\n", encoding="utf-8")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/status")
def status():
    resp = make_response(jsonify({"status": "ok"}))
    resp.headers["X-Internal-Path"] = str(INTERNAL_PATH)
    resp.headers["X-Env"] = "staging"
    return resp


@app.route("/hint-file")
def hint_file():
    return send_file(INTERNAL_PATH)


@app.route("/flag")
def flag():
    hint = request.args.get("hint", "")
    if hint == HINT_VALUE:
        return FLAG
    return "forbidden", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
