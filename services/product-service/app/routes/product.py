from fastapi import APIRouter
from cache.redis_client import redis_client
import json

router = APIRouter()

products_db = [
    {"id": 1, "name": "Laptop", "price": 1000},
    {"id": 2, "name": "Phone", "price": 500}
]


@router.get("/")
def get_products():

    cached_products = redis_client.get("products")

    if cached_products:
        print("Cache hit")
        return json.loads(cached_products)

    print("Cache miss")

    redis_client.set("products", json.dumps(products_db), ex=60)

    return products_db