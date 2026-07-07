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


@app.delete("/products/{index}")
def delete_product(index: int):
    if index < 0 or index >= len(products):
        raise HTTPException(status_code=404, detail="Product not found")
    deleted = products.pop(index)
    return {"message": "Deleted", "product": deleted}