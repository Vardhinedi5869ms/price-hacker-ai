from fastapi import FastAPI
from pydantic import BaseModel
import random
from typing import List, Dict

app = FastAPI()

# Simulate some products
products_data = {
    "amazon": [
        {"name": "Laptop", "price": 50000},
        {"name": "Phone", "price": 15000},
        {"name": "Headphones", "price": 3000},
    ],
    "flipkart": [
        {"name": "Shirt", "price": 1000},
        {"name": "Pants", "price": 2000},
        {"name": "Watch", "price": 4000},
    ],
    "ajio": [
        {"name": "Sunglasses", "price": 1200},
        {"name": "Shoes", "price": 3000},
        {"name": "Bags", "price": 1500},
    ],
    "myntra": [
        {"name": "Jacket", "price": 5000},
        {"name": "T-shirt", "price": 800},
        {"name": "Jeans", "price": 2000},
    ]
}

# API route to fetch products for the selected platform
@app.get("/get-products/{platform}")
async def get_products(platform: str):
    platform = platform.lower()
    if platform in products_data:
        return products_data[platform]
    return []  # Return empty list if platform is not found
