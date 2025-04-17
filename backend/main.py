from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample product data for platforms
mock_products = {
    "amazon": [
        {"name": "Study Table", "price": 1200},
        {"name": "Laptop Stand", "price": 900},
        {"name": "Desk Lamp", "price": 400}
    ],
    "flipkart": [
        {"name": "Office Chair", "price": 3000},
        {"name": "Bookshelf", "price": 2000},
        {"name": "Table Mat", "price": 150}
    ],
    "ajio": [
        {"name": "New Balance", "price": 10000},
        {"name": "Nike Air Max", "price": 12000},
        {"name": "Adidas Ultraboost", "price": 15000}
    ],
    "myntra": [
        {"name": "Puma Running Shoes", "price": 8000},
        {"name": "Reebok Classic", "price": 7000},
        {"name": "Under Armour", "price": 9000}
    ],
}

# API Input Model
class NegotiationRequest(BaseModel):
    platform: str
    product: str
    original_price: float
    target_price: float
    seller_type: str
    quantity: int
    is_loyal_customer: bool
    renegotiation_round: int = 0  # New field: default = 0

# API: Get products for a platform
@app.get("/get-products/{platform}")
def get_products(platform: str):
    return mock_products.get(platform.lower(), [])

# API: Negotiate logic
@app.post("/negotiate/")
def negotiate(data: NegotiationRequest):
    # Base discount
    discount = 0
    if data.seller_type == "retail":
        discount += 5
    if data.is_loyal_customer:
        discount += 3
    if data.quantity >= 10:
        discount += 10
    elif data.quantity >= 5:
        discount += 5

    # Renegotiation bonus (max 2 rounds)
    if data.renegotiation_round == 1:
        discount += 2
    elif data.renegotiation_round >= 2:
        discount += 1

    total_price = data.original_price * data.quantity
    negotiated_price = round(total_price * (1 - discount / 100), 2)

    return {
        "product": data.product,
        "platform": data.platform,
        "negotiated_price": negotiated_price,
        "discount_percent": discount,
        "affiliate_link": f"https://affiliate.{data.platform.lower()}.com/{data.product.replace(' ', '-')}",
        "can_renegotiate": data.renegotiation_round < 2
    }
