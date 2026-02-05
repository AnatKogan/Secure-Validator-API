from flask import Flask, request, jsonify, render_template_string
import os
from datetime import datetime

app = Flask(__name__)

APP_SECRET = os.getenv("APP_SECRET", "changeme")
LOG_PATH = os.getenv("LOG_PATH", "/app/logs/success.log")

@app.get("/")
def index():
   
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Secure Validator</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: sans-serif; text-align: center; padding-top: 50px; background: #f4f4f9; }
                .card { background: white; padding: 20px; border-radius: 10px; display: inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
                input { padding: 10px; border: 1px solid #ddd; border-radius: 5px; width: 200px; }
                button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
                #result { margin-top: 20px; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>🔐 API Validator</h2>
                <p>Enter your secret key:</p>
                <input type="password" id="secret" placeholder="Secret...">
                <button onclick="send()">Verify</button>
                <div id="result"></div>
            </div>
            <script>
                async function send() {
                    const val = document.getElementById('secret').value;
                    const res = await fetch('/validate', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({value: val})
                    });
                    const data = await res.json();
                    const el = document.getElementById('result');
                    el.innerText = data.ok ? "✅ ACCESS GRANTED" : "❌ ACCESS DENIED";
                    el.style.color = data.ok ? "#28a745" : "#dc3545";
                }
            </script>
        </body>
        </html>
    ''')

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.post("/validate")
def validate():
    data = request.get_json(silent=True) or {}
    value = data.get("value")
    
    print(f"DEBUG: Received '{value}', Expected '{APP_SECRET}'")

    if value is None:
        return jsonify({"ok": False}), 400

    if str(value).strip() != str(APP_SECRET).strip():
        return jsonify({"ok": False}), 401

    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{datetime.utcnow().isoformat()}Z success\n")

    return jsonify({"ok": True}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)