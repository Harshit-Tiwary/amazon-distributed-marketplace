FROM python:3.11-slim

WORKDIR /app

COPY app /app

RUN pip install --no-cache-dir fastapi uvicorn redis pika httpx sqlalchemy

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]