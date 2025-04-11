def negotiate_price(original_price, platform, target_price, seller_type, quantity, is_loyal_customer):
    base_discount = 0.05
    if seller_type == "reseller":
        base_discount += 0.02
    if is_loyal_customer:
        base_discount += 0.03
    if quantity >= 5:
        base_discount += 0.04
    elif quantity >= 3:
        base_discount += 0.02
    elif quantity > 1:
        base_discount += 0.01

    discount_amount = original_price * base_discount
    negotiated_price = original_price - discount_amount

    return {
        "discount_percent": round(base_discount * 100, 2),
        "negotiated_price": round(negotiated_price, 2)
    }
