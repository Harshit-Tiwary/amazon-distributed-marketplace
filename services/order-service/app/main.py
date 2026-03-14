from fastapi import FastAPI
from messaging.rabbitmq import publish_event

app = FastAPI(title="Order Service")


@app.get("/")
def root():
    return {"message": "Order Service Running"}


@app.post("/create-order")
def create_order():
    order_data = {
        "order_id": 101,
        "product_id": 1,
        "quantity": 1,
        "status": "created"
    }

    publish_event("ORDER_CREATED", order_data)

    return {
        "message": "Order created and event published",
        "order": order_data
    }


@app.get("/health")
def health():
    return {"status": "healthy"}