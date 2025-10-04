import os
from flask import Flask, jsonify, render_template, request
from lxml import etree

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{xml_xxe_resource_exhaust}")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/api/import", methods=["POST"])
def import_xml():
    raw = request.data or request.form.get("xml", "").encode()
    if not raw:
        return jsonify({"error": "XML vazio"}), 400

    parser = etree.XMLParser(resolve_entities=True, load_dtd=True, no_network=False)
    try:
        root = etree.fromstring(raw, parser=parser)
        content = etree.tostring(root, pretty_print=True).decode()
    except Exception as exc:
        return jsonify({"error": f"Erro ao processar XML: {exc}"}), 400

    return jsonify({"status": "ok", "echo": content[:2000]})


@app.route("/api/sample")
def sample():
    xml = """<?xml version='1.0'?>\n<transfer><amount>2500</amount><account>123</account></transfer>"""
    return jsonify({"xml": xml})


@app.route("/flag")
def flag():
    return FLAG


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
