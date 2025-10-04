from flask import Flask, request, render_template
import os

app = Flask(__name__)
FLAG = "ITAU2025{path_traversal_master}"
APP_ROOT = "/app/data"


@app.route("/")
def index():
    files = []
    try:
        files = sorted(os.listdir(APP_ROOT))
    except FileNotFoundError:
        pass
    return render_template("index.html", files=files)


@app.route("/health")
def health():
    return "OK", 200


@app.route("/read")
def read():
    fname = request.args.get("file", "")
    if not fname:
        return "specify ?file="
    target = os.path.join(APP_ROOT, fname)
    try:
        with open(target, "rb") as handle:
            return handle.read(), 200
    except Exception as exc:
        return f"error: {exc}", 404


@app.route("/flag")
def flag():
    return FLAG


if __name__ == "__main__":
    os.makedirs(APP_ROOT, exist_ok=True)
    with open(os.path.join(APP_ROOT, "public.txt"), "w", encoding="utf-8") as handle:
        handle.write("public info\n")
    app.run(host="0.0.0.0", port=8080)
