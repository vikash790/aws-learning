from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Product(BaseModel):
    name: str
    price: float

products = []

@app.get("/products/")
def get_products():
    return products

@app.post("/products/")
def create_product(product: Product):
    products.append(product)
    return product