import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000"  # Make sure this matches your backend URL

def fetch_products(platform, current_value):
    if not platform:
        return gr.update(choices=[], value=None), {}
    
    try:
        # Send request to fetch products for the selected platform
        response = requests.get(f"{API_URL}/get-products/{platform.lower()}")
        if response.status_code == 200:
            products = response.json()
            names = [p["name"] for p in products]  # Extract product names
            prices = {p["name"]: p["price"] for p in products}  # Map product names to their prices
            value = current_value if current_value in names else (names[0] if names else None)
            return gr.update(choices=names, value=value), prices  # Update dropdown choices and prices dictionary
        return gr.update(choices=[], value=None), {}
    except Exception as e:
        return gr.update(choices=[], value=None), {}

def autofill_price(product_name, price_dict):
    return price_dict.get(product_name, 0)

def negotiate_price(platform, product, original_price, target_price, seller_type, quantity, is_loyal, attempts):
    payload = {
        "platform": platform,
        "product": product,
        "original_price": original_price,
        "target_price": target_price,
        "seller_type": seller_type,
        "quantity": quantity,
        "is_loyal_customer": is_loyal,
        "renegotiation_round": attempts  # Use attempts to track renegotiation
    }
    try:
        res = requests.post(f"{API_URL}/negotiate/", json=payload)
        res_data = res.json()
        return f"""✅ **Negotiation Summary** (Attempt {attempts}):
        🛍️ **Product:** {res_data['product']}
        🛒 **Platform:** {res_data['platform']}
        📦 **Quantity:** {quantity}
        💰 **Original Price (1 unit):** ₹{original_price}
        📊 **Total Original Price:** ₹{original_price * quantity:.2f}
        🎯 **Negotiated Total Price:** ₹{res_data['negotiated_price']:.2f}
        🔻 **Discount:** {res_data['discount_percent']}%
        💸 **You Saved:** ₹{original_price * quantity - res_data['negotiated_price']:.2f}
        🏷️ **Final Per Unit Price:** ₹{res_data['negotiated_price'] / quantity:.2f}
        🔗 [Click to Buy (Affiliate Link)]({res_data['affiliate_link']})
        """
    except Exception as e:
        return f"❌ Negotiation failed: {str(e)}"

# UI layout
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🤖 AI Price Negotiation Tool")

    with gr.Row():
        platform = gr.Dropdown(label="Platform", choices=["Amazon", "Flipkart", "Ajio", "Myntra"], value="Amazon")
        product = gr.Dropdown(label="Select Product", allow_custom_value=True)
    
    with gr.Row():
        original_price = gr.Number(label="Original Price", value=0)
        target_price = gr.Number(label="Your Target Price", value=0)

    with gr.Row():
        seller_type = gr.Radio(choices=["retail", "reseller"], value="retail", label="Seller Type")
        quantity = gr.Slider(minimum=1, maximum=100, step=1, value=1, label="Quantity")

    is_loyal = gr.Checkbox(label="Are you a loyal customer?")
    attempts = gr.Number(value=1, visible=False)  # Used internally for renegotiation tracking
    result_box = gr.Markdown()

    prices_dict = gr.State({})

    # Fetch product list when platform changes
    platform.change(fetch_products, inputs=[platform, product], outputs=[product, prices_dict])

    # Autofill price when product changes
    product.change(autofill_price, inputs=[product, prices_dict], outputs=original_price)

    negotiate_btn = gr.Button("Negotiate Price 💬")
    renegotiate_btn = gr.Button("Renegotiate 🤝")

    negotiate_btn.click(
        negotiate_price,
        inputs=[platform, product, original_price, target_price, seller_type, quantity, is_loyal, attempts],
        outputs=result_box
    )

    def increase_attempt(current):
        return current + 1

    renegotiate_btn.click(increase_attempt, inputs=attempts, outputs=attempts).then(
        negotiate_price,
        inputs=[platform, product, original_price, target_price, seller_type, quantity, is_loyal, attempts],
        outputs=result_box
    )

demo.launch()
