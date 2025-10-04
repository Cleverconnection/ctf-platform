import os
from copy import deepcopy
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{account_merge_disclosure}")
accounts = {
    "1001": {"id": "1001", "owner": "Cliente Standard", "notes": "saldo regular"},
    "2300": {"id": "2300", "owner": "Agência Digital", "notes": "conta compartilhada"},
    "7777": {"id": "7777", "owner": "Executivo", "notes": FLAG},
}


@app.route("/")
def index():
    return render_template("index.html", accounts=list(accounts.values()))


@app.route("/health")
def health():
    return "OK", 200


@app.route("/api/accounts")
def list_accounts():
    return jsonify({"accounts": list(accounts.values())})


@app.route("/api/merge", methods=["POST"])
def merge():
    data = request.get_json() or {}
    primary = data.get("primary")
    secondary = data.get("secondary")

    if primary not in accounts or secondary not in accounts:
        return jsonify({"error": "conta inválida"}), 404

    if primary == secondary:
        return jsonify({"error": "contas iguais"}), 400

    merged = deepcopy(accounts[primary])
    donor = accounts[secondary]
    merged["notes"] += f"; anexado {donor['owner']}"
    accounts.pop(secondary)
    accounts[primary] = merged

    return jsonify({"status": "ok", "merged": {"primary": merged, "secondary": donor}})


@app.route("/flag")
def flag():
    return "Restrito ao sistema de fusão", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
