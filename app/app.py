from flask import Flask, request, jsonify
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

APP_SECRET = os.getenv("APP_SECRET", "1234")
LOG_PATH = os.getenv("LOG_PATH", "logs/success.log")
PORT = int(os.getenv("PORT", 8080))

@app.get("/")
def index():
    return jsonify({"message": "Secure Validator API is running"}), 200

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.post("/validate")
def validate():
    data = request.get_json(silent=True)
    user_value = data.get('value') if data else "None"
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    is_valid = str(user_value).strip() == str(APP_SECRET).strip()

    if is_valid:
        # Log SUCCESS to file
        try:
            log_dir = os.path.dirname(LOG_PATH)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)

            with open(LOG_PATH, "a", encoding="utf-8") as f:
                f.write(f"{timestamp} | IP: {client_ip} | Status: success\n")
                f.flush()
        except Exception as e:
            print(f"Logging failed: {e}")
        
        return jsonify({"ok": True}), 200
    
    else:
        # Print FAILURE to console only
        print(f"ALERT: Failed validation attempt at {timestamp} | IP: {client_ip} | Value: {user_value}")
        return jsonify({"ok": False}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)