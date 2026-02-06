FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/app.py .

RUN mkdir -p /app/logs && chown -R 1000:1000 /app/logs

RUN useradd -m -u 1000 appuser
USER 1000

ENV PORT=8080
EXPOSE 8080

CMD ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "-b", "0.0.0.0:8080", "app:app"]