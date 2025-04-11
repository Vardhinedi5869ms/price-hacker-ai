import gradio as gr
import requests

product_cache = {}

def fetch_products(platform):
    if platform.lower() == "amazon":
        return [
            {"name": "iPhone 15", "price": 80000},
            {"name": "MacBook Air", "price": 110000},
            {"name": "Noise Smartwatch", "price": 4000}
        ]
    elif platform.lower() == "flipkart":
        return [
            {"name": "Realme Narzo", "price": 15000},
            {"name": "Boat Airdopes", "price": 2000},
            {"name": "Dell Laptop", "price": 75000}
        ]
    return []

def update_products(platform):
    print(f"[DEBUG] Platform selected: {platform}")
    products = fetch_products(platform)
    print(f"[DEBUG] Products fetched: {products}")
    product_cache[platform] = products
    return gr.update(choices=[p["name"] for p in products], value=None)

def fill_original_price(product_name, platform):
    products = product_cache.get(platform, [])
    for p in products:
        if p["name"] == product_name:
            return p["price"]
    return 0.0

def negotiate(product_name, platform, original_price, target_price, seller_type, quantity, is_loyal_customer):
    payload = {
        "product_name": product_name,
        "original_price": original_price,
        "platform": platform,
        "target_price": target_price,
        "seller_type": seller_type,
        "quantity": quantity,
        "is_loyal_customer": is_loyal_customer
    }
    try:
        response = requests.post("http://127.0.0.1:8000/negotiate", json=payload)
        result = response.json()

        return f"""✅ Negotiation Summary:

🛍️ Product: {result['product']}
🛒 Platform: {result['platform']}
📦 Quantity: {result['quantity']}
💰 Original Price (1 unit): ₹{result['original_price']}
📊 Total Original Price: ₹{result['total_price']}
🎯 Negotiated Total Price: ₹{result['negotiated_price']}
🔻 Discount: {result['discount_percent']}%
💸 You Saved: ₹{result['you_saved']}
🏷️ Final Per Unit Price: ₹{result['final_per_unit_price']}"""
    except Exception as e:
        return f"❌ Error: {str(e)}"

with gr.Blocks(title="Price Negotiation Tool") as demo:
    gr.Markdown("## 🤖 AI Price Negotiation Tool")
    with gr.Row():
        platform = gr.Dropdown(choices=["Amazon", "Flipkart"], label="Select Platform")
        product_name = gr.Dropdown(choices=[], label="Select Product")
        platform.change(fn=update_products, inputs=platform, outputs=product_name)
        product_name.change(fn=fill_original_price, inputs=[product_name, platform], outputs=None)

    original_price = gr.Number(label="Original Price (auto-filled or manual)")
    target_price = gr.Number(label="Target Price")
    seller_type = gr.Radio(choices=["retail", "reseller","business","brand",], label="Seller Type", value="retail")
    quantity = gr.Slider(1, 100, value=1, label="Quantity")
    is_loyal_customer = gr.Checkbox(label="Loyal Customer?")
    submit = gr.Button("Negotiate 🔥")
    output = gr.Textbox(label="Result")

    product_name.change(fn=fill_original_price, inputs=[product_name, platform], outputs=original_price)
    submit.click(
        negotiate,
        inputs=[product_name, platform, original_price, target_price, seller_type, quantity, is_loyal_customer],
        outputs=output
    )

demo.launch()
