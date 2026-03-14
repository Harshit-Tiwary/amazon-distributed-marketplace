from fastapi import FastAPI
from app.database import engine, Base
from app.models import product
from app.messaging.rabbitmq import publish_event

app = FastAPI(
    title="Product Service",
    description="Product Catalog Service",
    version="1.0"
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Product Service Running"}


@app.post("/create-product")
def create_product():

    product_data = {
        "id": 1,
        "name": "Laptop",
        "price": 1000
    }

    publish_event("PRODUCT_CREATED", product_data)

    return {
        "message": "Product created and event published"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}