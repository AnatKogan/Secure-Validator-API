## Project Structure
Secure Validator API/
├── app/
│   ├── app.py              # Main Flask application
│   └── requirements.txt    # Python dependencies
├── docker/
│   └── Dockerfile          # Multi-stage container config
├── logs/                   # Success logs (Created by Docker)
└── docker-compose.yaml     # Local orchestration

Secure Validator API
A Flask-based API designed to demonstrate DevOps practices, including containerization, cloud deployment, and infrastructure monitoring.

Key Features
Dockerized Environment: Fully containerized using Docker and managed with Docker Compose.

Cloud Native: Deployed on Google Cloud Run with centralized logging.

Dynamic Health Monitoring: Includes a custom /health endpoint that performs deep checks on the container file system.

Environment Management: Uses environment variables for configuration and secrets.

Live Infrastructure
Application Interface: https://secure-validator-service-223990326824.me-west1.run.app/validate

Health Monitoring: https://secure-validator-service-223990326824.me-west1.run.app/health

Health Check Logic
The application implements a dynamic health check to ensure reliability:

It verifies that the logs directory exists within the container.

It confirms that the application has active write permissions to the file system.

In case of failure (e.g., directory missing or permission issues), the endpoint returns a 500 status code with a JSON error report, allowing the cloud orchestrator to handle the instance accordingly.

Local Deployment
Clone the repository to your local machine.

Ensure Docker Desktop is running.

Execute the following command in the project root:
docker-compose up --build

Access the local instance at:

Application: http://localhost:8080/validate

Health Status: http://localhost:8080/health
