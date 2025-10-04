from flask import Flask, request, Response, render_template
import requests

app = Flask(__name__)
FLAG = "ITAU2025{ssrf_proxy_to_flag}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/fetch")
def fetch():
    url = request.args.get("url", "")
    if not url:
        return "provide ?url=", 400
    try:
        r = requests.get(url, timeout=5)
        return Response(
            r.content,
            status=r.status_code,
            content_type=r.headers.get("Content-Type", "text/plain"),
        )
    except Exception as exc:
        return f"error: {exc}", 500


@app.route("/flag")
def flag():
    return FLAG


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
