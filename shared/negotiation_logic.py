# negotiation_logic.py

import random

def negotiate(req):
    original_price = req.original_price
    target_price = req.target_price
    quantity = req.quantity
    seller_type = req.seller_type
    is_loyal = req.is_loyal_customer
    round_num = req.renegotiation_round

    base_discount = 5

    if target_price < original_price:
        base_discount += ((original_price - target_price) / original_price) * 10

    if quantity > 5:
        base_discount += 5

    if is_loyal:
        base_discount += 3

    if seller_type == "reseller":
        base_discount += 2

    # Adjust based on renegotiation rounds
    if round_num == 2:
        base_discount += 2
    elif round_num >= 3:
        base_discount += 1

    # Add randomness
    base_discount += random.uniform(-1, 1)

    # Cap between 5% to 35%
    discount = max(5, min(base_discount, 35))
    total_price = original_price * quantity
    negotiated_price = total_price * (1 - discount / 100)

    affiliate_link = generate_affiliate_link(req.platform, req.product)

    return {
        "platform": req.platform,
        "product": req.product,
        "negotiated_price": round(negotiated_price, 2),
        "discount_percent": round(discount, 2),
        "affiliate_link": affiliate_link
    }

def generate_affiliate_link(platform, product):
    base_urls = {
        "amazon": "https://amzn.to/demo-affiliate",
        "flipkart": "https://fkrt.it/demo-affiliate",
        "zomato": "https://zoma.to/demo-affiliate",
        "swiggy": "https://swig.gy/demo-affiliate",
        "saas": "https://saas.com/demo-affiliate"
    }
    return base_urls.get(platform.lower(), "https://default.com")
