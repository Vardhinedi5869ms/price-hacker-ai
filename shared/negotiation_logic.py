# shared/negotiation_logic.py

def calculate_discount(platform, seller_type, quantity, is_loyal):
    """
    Determines the discount percentage based on platform, seller type, quantity, and loyalty.
    """
    discount = 0

    # Platform base discounts
    platform_discounts = {
        "amazon": 5,
        "flipkart": 4,
        "ajio": 6,
        "myntra": 5,
    }
    discount += platform_discounts.get(platform.lower(), 3)

    # Seller type effect
    if seller_type == "reseller":
        discount += 5
    elif seller_type == "retail":
        discount += 2

    # Quantity tiers
    if quantity >= 10:
        discount += 7
    elif quantity >= 5:
        discount += 4
    elif quantity > 1:
        discount += 2

    # Loyalty bonus
    if is_loyal:
        discount += 3

    return discount

def calculate_negotiated_price(original_price, quantity, discount_percent):
    """
    Calculates total and per-unit prices after applying discount.
    """
    total_price = original_price * quantity
    discounted_total = total_price * (1 - discount_percent / 100)
    per_unit_price = discounted_total / quantity
    savings = total_price - discounted_total

    return {
        "total_original_price": round(total_price, 2),
        "negotiated_price": round(discounted_total, 2),
        "per_unit_price": round(per_unit_price, 2),
        "savings": round(savings, 2),
        "discount_percent": round(discount_percent, 2)
    }
