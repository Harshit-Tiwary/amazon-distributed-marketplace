FROM python:3.11-slim

WORKDIR /app

COPY app /app

RUN pip install --no-cache-dir fastapi uvicorn pika httpx

EXPOSE 8002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]