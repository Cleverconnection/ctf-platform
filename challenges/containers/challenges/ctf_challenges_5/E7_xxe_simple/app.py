from flask import Flask, request, render_template, jsonify
import os
from pathlib import Path
from lxml import etree

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{xxe_into_core}")
DATA_DIR = Path("/app/data")
SECRET_CODE_PATH = DATA_DIR / "xxe_secret.txt"
ACCESS_CODE = "xml-core-2025"

DATA_DIR.mkdir(parents=True, exist_ok=True)
if not SECRET_CODE_PATH.exists():
    SECRET_CODE_PATH.write_text(f"code={ACCESS_CODE}\n", encoding="utf-8")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/upload", methods=["POST"])
def upload():
    xml_payload = request.form.get("xml", "")
    if not xml_payload:
        return jsonify({"error": "corpo XML vazio"}), 400
    try:
        parser = etree.XMLParser(resolve_entities=True)
        doc = etree.fromstring(xml_payload.encode("utf-8"), parser)
        customer = doc.findtext("customer", default="desconhecido")
        message = doc.findtext("message", default="")
        return jsonify({"customer": customer, "message": message})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/flag")
def flag():
    code = request.args.get("code", "")
    if code == ACCESS_CODE:
        return FLAG
    return "forbidden", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
