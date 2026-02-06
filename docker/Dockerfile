FROM python:3.9-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

RUN mkdir -p /app/logs

EXPOSE 8080

CMD ["python", "app.py"]