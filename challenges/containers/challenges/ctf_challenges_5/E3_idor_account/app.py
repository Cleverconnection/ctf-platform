from flask import Flask, jsonify, render_template

app = Flask(__name__)
FLAG = "ITAU2025{idor_bank_accounts}"

ACCOUNTS = {
    "1": {"id": "1", "owner": "bob", "balance": 100},
    "42": {"id": "42", "owner": "ceo", "balance": 1_000_000, "note": "FLAG_HERE"},
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/accounts/<accid>")
def account(accid):
    acc = ACCOUNTS.get(accid)
    if not acc:
        return jsonify({"error": "not found"}), 404
    data = dict(acc)
    if accid == "42":
        data["flag"] = FLAG
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
