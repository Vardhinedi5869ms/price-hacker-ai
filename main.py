from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_model import predict_price  # Import AI function
from datetime import datetime

app = FastAPI()

class PriceNegotiationRequest(BaseModel):
    product_name: str
    original_price: float
    target_price: float
    seller_type: str
    quantity: int  # New field for bulk discount
    is_loyal_customer: bool  # New field for loyalty discount

@app.get("/")
def home():
    return {"message": "Welcome to Price Hacker AI"}

def calculate_discounted_price(original_price: float, target_price: float, seller_type: str, quantity: int, is_loyal_customer: bool) -> dict:
    discount = 0  

    # Seller-based discount
    if seller_type == "retailer":
        discount += 5  
    elif seller_type == "wholesaler":
        discount += 10  

    # Bulk purchase discount
    if quantity >= 5:
        discount += 3
    if quantity >= 10:
        discount += 5

    # Seasonal discount (e.g., festival sales)
    current_month = datetime.now().month
    if current_month in [11, 12]:  # November, December (Holiday Sales)
        discount += 7

    # Loyalty discount
    if is_loyal_customer:
        discount += 4

    # Ensure total discount does not exceed 25%
    total_discount = min(discount, 25)
    
    # Calculate discounted price
    discounted_price = original_price * (1 - total_discount / 100)
    
    return {
        "original_price": original_price,
        "negotiated_price": round(discounted_price, 2),
        "discount_applied": f"{total_discount}%"
    }

@app.post("/negotiate")
def negotiate_price(request: PriceNegotiationRequest):
    # Validate input
    if request.original_price <= 0:
        raise HTTPException(status_code=400, detail="Invalid price")
    if request.target_price <= 0:
        raise HTTPException(status_code=400, detail="Invalid target price")
    if request.quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")

    # Calculate discount-based price
    discount_result = calculate_discounted_price(
        request.original_price, 
        request.target_price, 
        request.seller_type, 
        request.quantity, 
        request.is_loyal_customer
    )

    # AI model prediction
    ai_predicted_price = predict_price(request.original_price, request.target_price)

    # Final negotiated price = Max(AI Prediction, Discounted Price)
    final_price = max(ai_predicted_price, discount_result["negotiated_price"])

    return {
        "product": request.product_name,
        "original_price": request.original_price,
        "negotiated_price": round(final_price, 2),
        "discount_applied": discount_result["discount_applied"],
        "ai_predicted_price": ai_predicted_price
    }
