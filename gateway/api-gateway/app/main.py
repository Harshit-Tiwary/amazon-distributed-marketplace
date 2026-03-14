from fastapi import FastAPI, Request
import httpx

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.responses import JSONResponse

from tenacity import retry, stop_after_attempt, wait_fixed


limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Marketplace API Gateway")

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    lambda request, exc: JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
    ),
)

app.add_middleware(SlowAPIMiddleware)


PRODUCT_SERVICE = "http://127.0.0.1:8001"
ORDER_SERVICE = "http://127.0.0.1:8002"

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def call_get_service(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def call_post_service(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(url)
        response.raise_for_status()
        return response.json()


@app.get("/")
def root():
    return {"message": "API Gateway Running"}

@app.get("/products")
@limiter.limit("10/minute")
async def get_products(request: Request):

    data = await call_get_service(f"{PRODUCT_SERVICE}/")
    return data

@app.post("/orders")
@limiter.limit("5/minute")
async def create_order(request: Request):

    data = await call_post_service(f"{ORDER_SERVICE}/create-order")
    return data