import os
from pathlib import Path
from flask import Flask, jsonify, render_template, send_from_directory

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{supply_chain_artifact}")
ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
ARTIFACT_FILE = ARTIFACT_DIR / "runner.log"


def ensure_artifact():
    ARTIFACT_DIR.mkdir(exist_ok=True)
    content = """Pipeline: release-candidate\nStatus: success\nImage pushed: registry.devops/itau/core:2025.04\nSecret token: {flag}\n""".format(flag=FLAG)
    ARTIFACT_FILE.write_text(content)


ensure_artifact()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/api/pipelines/latest")
def latest():
    ensure_artifact()
    return jsonify({
        "pipeline": "release-candidate",
        "status": "success",
        "artifact": "/artifact/runner.log",
        "size": ARTIFACT_FILE.stat().st_size,
    })


@app.route("/artifact/<path:name>")
def artifact(name):
    ensure_artifact()
    return send_from_directory(ARTIFACT_DIR, name, as_attachment=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
