import os
import sys
from flask import Flask, request, render_template_string, jsonify
from datetime import datetime

app = Flask(__name__)

LOG_FILE = "/app/logs/success.log"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Secure Validator</title>
    <style>
        body { background-color: #f0f2f5; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; width: 350px; }
        h2 { margin-bottom: 25px; color: #1c1e21; font-size: 24px; }
        input { width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; font-size: 16px; }
        button { width: 100%; padding: 12px; background-color: #007bff; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; transition: background 0.2s; }
        button:hover { background-color: #0056b3; }
        .message { margin-top: 20px; font-weight: bold; display: flex; align-items: center; justify-content: center; gap: 8px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>DevOps Secure Login</h2>
        <form action="/validate" method="get">
            <input type="text" name="key" placeholder="Username" required>
            <input type="password" name="value" placeholder="Secret" required>
            <button type="submit">Validate</button>
        </form>
        {% if msg %}
        <div class="message" style="color: {{ color }};">
            <span>{{ icon }}</span> {{ msg }}
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/validate')
def validate():
    user_key = request.args.get('key')
    user_val = request.args.get('value')
    
    if not user_key or not user_val:
        return render_template_string(HTML_TEMPLATE)

    correct_key = os.getenv('REQUIRED_KEY', 'admin')
    correct_val = os.getenv('APP_SECRET')

    if user_key == correct_key and user_val == correct_val:
        # Get the real user IP from X-Forwarded-For if it exists, otherwise use remote_addr
        forwarded_ip = request.headers.get('X-Forwarded-For')
        if forwarded_ip:
            client_ip = forwarded_ip.split(',')[0]
        else:
            client_ip = request.remote_addr or "unknown"

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{current_time}] SUCCESS: User '{user_key}' from IP {client_ip}\n"
        
        try:
            os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
            with open(LOG_FILE, "a") as f:
                f.write(log_entry)
                f.flush()
            
            # Print to stderr for Google Cloud Logs Explorer
            print(log_entry.strip(), file=sys.stderr)
            
            return render_template_string(HTML_TEMPLATE, msg="Access Granted & Logged", color="#28a745", icon="✔")
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, msg=f"Log Error: {e}", color="#ffc107", icon="⚠")

    return render_template_string(HTML_TEMPLATE, msg="Invalid Credentials", color="#dc3545", icon="✘")

@app.route('/health')
def health_check():
    log_dir = 'logs'
    is_writable = os.access(log_dir, os.W_OK)
    
    if not is_writable:
        return jsonify(
            status="unhealthy", 
            reason="Log directory is not writable",
            container="secure-validator"
        ), 500
        
    return jsonify(
        status="healthy", 
        container="secure-validator"
    ), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)