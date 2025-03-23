from fastapi import FastAPI
from pydantic import BaseModel
from ai_model import predict_price  # Import AI function

app = FastAPI()

class PriceNegotiationRequest(BaseModel):
    product_name: str
    original_price: float
    target_price: float

@app.get("/")
def home():
    return {"message": "Welcome to Price Hacker AI"}

@app.post("/negotiate")
def negotiate_price(request: PriceNegotiationRequest):
    """
    Uses AI to negotiate the best price.
    """
    ai_price = predict_price(request.original_price, request.target_price)

    return {
        "product": request.product_name,
        "original_price": request.original_price,
        "negotiated_price": ai_price
    }
