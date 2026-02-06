FROM python:3.12-slim

# Prevent buffering for immediate logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/app.py .

# Security and logging setup
RUN mkdir -p /app/logs
RUN useradd -m -u 1000 appuser && chown -R 1000:1000 /app
USER 1000

ENV PORT=8080
EXPOSE 8080

# Run with Gunicorn and redirect logs to stdout
CMD ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "-b", "0.0.0.0:8080", "app:app"]