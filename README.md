# Secure Validator API

A lightweight Python microservice that validates a user-provided value against a secret and logs the client IP on success.

## Endpoints
- GET /health
- POST /validate

## Local run
```bash
export APP_SECRET=1234
pip install -r app/requirements.txt
python app/app.py
