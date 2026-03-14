from locust import HttpUser, task

class User(HttpUser):

    @task
    def get_products(self):
        self.client.get("/products")

    @task
    def create_order(self):
        self.client.post("/orders", json={
            "product_id":1,
            "quantity":1
        })