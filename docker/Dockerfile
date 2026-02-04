FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/app.py /app/app.py

RUN mkdir -p /app/logs

RUN useradd -m -u 1000 appuser && chown -R 1000:1000 /app
USER 1000

ENV PORT=8080
EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
