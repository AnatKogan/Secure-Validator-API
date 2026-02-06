# Secure Validator API

A professional Dockerized Python API built with Flask and Gunicorn. This project demonstrates secure key validation, environment variable management, and advanced logging practices.

---

## Features
- Validation Endpoint: Securely check values via POST /validate.
- Standardized Logging:
    - Successes: Logged to a local file (logs/success.log) via Docker Volumes.
    - Security Alerts: Failed attempts are printed to stdout for real-time monitoring.
- Production Ready: Runs using Gunicorn with non-root user security.
- DevOps Best Practices: Zero-buffering logs and automated container restarts.

---

## Project Structure
Secure Validator API/
├── app/
│   ├── app.py              # Main Flask application
│   └── requirements.txt    # Python dependencies
├── docker/
│   └── Dockerfile          # Multi-stage container config
├── logs/                   # Success logs (Created by Docker)
└── docker-compose.yaml     # Local orchestration

---

## Getting Started

### 1. Prerequisites
Make sure you have Docker Desktop installed and running on your machine.

### 2. Run Locally
Execute the following command in your terminal from the project root:
docker-compose up -d --build

### 3. Verify Application
Check if the server is healthy by visiting:
http://localhost:8080/health

---

## Testing the API

### Success Scenario (Valid Secret)
Returns {"ok": true} and writes a log entry to the local logs folder.
Invoke-RestMethod -Uri "http://localhost:8080/validate" -Method Post -ContentType "application/json" -Body '{"value": "1234"}'

### Failure Scenario (Invalid Secret)
Returns {"ok": false} and triggers a real-time ALERT in the terminal.
Invoke-RestMethod -Uri "http://localhost:8080/validate" -Method Post -ContentType "application/json" -Body '{"value": "wrong-secret"}'

---

## Monitoring
To watch logs and security alerts in real-time, use the following command:
docker logs -f my-api

---

## Cloud Deployment
This project is pre-configured for Google Cloud Platform (GCP).
Deployment targets: Artifact Registry and Cloud Run.

Required Command:
gcloud run deploy secure-api --source .