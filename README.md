# Amazon-Style Distributed Marketplace (Microservices)

A production-style distributed backend system built using **FastAPI, Docker, RabbitMQ, Redis, and Microservices architecture**.

This project demonstrates how large-scale systems like Amazon or Uber structure backend services.

---

# Architecture

Client requests flow through an API Gateway which communicates with multiple backend services.

Services communicate asynchronously using RabbitMQ events.

Redis is used for caching to reduce latency.

---

# System Architecture

```
![Architecture](docs/architecture.png)
---

# Tech Stack

* FastAPI
* Python
* Docker
* RabbitMQ
* Redis
* Microservices Architecture
* Event-Driven Architecture

---

# Services

### API Gateway

Routes external requests to internal services.

### Product Service

Handles product catalog.

### Order Service

Handles order creation and publishes events.

### Inventory Service

Consumes order events and updates stock.

### Payment Service

Handles payment processing.

### Notification Service

Sends notifications after order completion.

---

# Running the System

Start all services using Docker:

```
docker compose up --build
```

API Gateway:

```
http://localhost:9000/docs
```

Product Service:

```
http://localhost:8001/docs
```

Order Service:

```
http://localhost:8002/docs
```

RabbitMQ Dashboard:

```
http://localhost:15672
```

Login:

```
username: guest
password: guest
```

---

# Event Flow

```
Create Order
     ↓
Order Service
     ↓
RabbitMQ Event
     ↓
Inventory Service
     ↓
Payment Service
     ↓
Notification Service
```

---

# Features

* Distributed Microservices
* Event-Driven Architecture
* Redis Caching
* RabbitMQ Messaging
* API Gateway Pattern
* Dockerized Infrastructure
* Swagger API Documentation

---

# Future Improvements

* Distributed rate limiting
* Circuit breaker pattern
* Service discovery
* Load testing
* Observability (Prometheus + Grafana)