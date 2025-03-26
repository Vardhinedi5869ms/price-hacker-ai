from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Enable CORS to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/negotiate")
async def negotiate_price(request: Request):
    data = await request.json()
    
    # Extract values
    original_price = data["original_price"]
    target_price = data["target_price"]
    seller_type = data["seller_type"]
    quantity = data["quantity"]
    is_loyal_customer = data["is_loyal_customer"]

    # Simple negotiation logic (replace with AI model later)
    discount = 0.05 if is_loyal_customer else 0.02
    if seller_type == "wholesaler":
        discount += 0.05
    if quantity > 10:
        discount += 0.03
    
    negotiated_price = original_price * (1 - discount)
    ai_predicted_price = max(target_price, negotiated_price)  # Placeholder AI logic
    
    return {"negotiated_price": round(negotiated_price, 2), "ai_predicted_price": round(ai_predicted_price, 2), "discount_applied": f"{discount*100}%"}
