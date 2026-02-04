from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

APP_SECRET = os.getenv("APP_SECRET", "changeme")
LOG_PATH = os.getenv("LOG_PATH", "/app/logs/success.log")

def get_client_ip():
    xff = request.headers.get("X-Forwarded-For", "")
    if xff:
        return xff.split(",")[0].strip()
    return request.remote_addr or "unknown"

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.post("/validate")
def validate():
    data = request.get_json(silent=True) or {}
    value = data.get("value")

    if value is None:
        return jsonify({"ok": False}), 400

    if str(value) != str(APP_SECRET):
        return jsonify({"ok": False}), 401

    ip = get_client_ip()
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{datetime.utcnow().isoformat()}Z ip={ip}\n")

    return jsonify({"ok": True}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

