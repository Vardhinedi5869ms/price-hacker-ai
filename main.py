from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_model import predict_price  # Import AI function

app = FastAPI()

class PriceNegotiationRequest(BaseModel):
    product_name: str
    original_price: float
    target_price: float
    seller_type: str

@app.get("/")
def home():
    return {"message": "Welcome to Price Hacker AI"}

@app.post("/negotiate")
def negotiate_price(request: PriceNegotiationRequest):
    discount_rate = 0.1 if request.seller_type == "wholesaler" else 0.05
    negotiated_price = max(request.target_price, request.original_price * (1 - discount_rate))
    
    discount_reason = "Wholesaler discount applied" if request.seller_type == "wholesaler" else "Retailer discount applied"

    return {
        "product": request.product_name,
        "original_price": request.original_price,
        "negotiated_price": round(negotiated_price, 2),
        "discount_reason": discount_reason
    }