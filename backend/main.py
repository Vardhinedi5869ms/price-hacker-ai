# main.py (fully updated)

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from shared.negotiation_logic import negotiate


app = FastAPI()

# Mock product data
mock_products = {
    "amazon": ["Logitech Mouse", "iPhone Charger", "Study Table"],
    "flipkart": ["Redmi Phone", "Backpack", "Washing Machine"],
    "zomato": ["Pizza Combo", "Burger Meal", "Family Dinner Pack"],
    "swiggy": ["Biryani Combo", "Dessert Box", "Healthy Meal Bowl"],
    "saas": ["Canva Pro", "Notion AI", "Grammarly Premium"]
}

mock_prices = {
    "Logitech Mouse": 500,
    "iPhone Charger": 1200,
    "Study Table": 3000,
    "Redmi Phone": 10000,
    "Backpack": 1500,
    "Washing Machine": 25000,
    "Pizza Combo": 399,
    "Burger Meal": 299,
    "Family Dinner Pack": 799,
    "Biryani Combo": 349,
    "Dessert Box": 249,
    "Healthy Meal Bowl": 399,
    "Canva Pro": 499,
    "Notion AI": 699,
    "Grammarly Premium": 899,
}

# API: Get products by platform
@app.get("/get-products/{platform}")
async def get_products(platform: str):
    platform = platform.lower()
    if platform in mock_products:
        products = mock_products[platform]
        return [{"name": p, "price": mock_prices.get(p, 0)} for p in products]
    return []

# Request model for negotiation
class NegotiationRequest(BaseModel):
    platform: str
    product: str
    original_price: float
    target_price: float
    quantity: int
    seller_type: str
    is_loyal_customer: bool
    renegotiation_round: int

# API: Negotiate price
@app.post("/negotiate/")
async def negotiate_price(req: NegotiationRequest):
    try:
        result = negotiate(req)
        return result
    except Exception as e:
        return {"error": str(e)}
