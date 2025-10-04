from flask import Flask, request, jsonify, render_template
import os
import sqlite3
from pathlib import Path

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "ITAU2025{sqli_in_the_branch}")
DB_PATH = Path("/app/data.db")
ACCESS_TOKEN = "E6-ACCESS-2025"


def init_db():
    created = not DB_PATH.exists()
    conn = sqlite3.connect(DB_PATH)
    if created:
        schema_sql = """
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                product TEXT NOT NULL,
                notes TEXT
            );
            CREATE TABLE secrets (
                code TEXT NOT NULL,
                token TEXT NOT NULL
            );
            INSERT INTO customers (name, product, notes) VALUES
                ('Bruna', 'Conta Salário', 'Sem observações'),
                ('Carlos', 'Conta PJ', 'Cliente novo, monitorar limites'),
                ('Equipe Auditoria', 'Conta Especial', 'Acesso restrito');
        """
        conn.executescript(schema_sql)
        conn.execute(
            "INSERT INTO secrets (code, token) VALUES (?, ?)",
            ("flag_access", ACCESS_TOKEN),
        )
        conn.commit()
    conn.close()


init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/search")
def search():
    q = request.args.get("q", "")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        query = f"SELECT name, product, notes FROM customers WHERE name LIKE '%{q}%'"
        rows = conn.execute(query).fetchall()
    except Exception as exc:
        conn.close()
        return jsonify({"error": str(exc)}), 400
    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route("/flag")
def flag():
    token = request.args.get("access_token", "")
    if token == ACCESS_TOKEN:
        return FLAG
    return "forbidden", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
