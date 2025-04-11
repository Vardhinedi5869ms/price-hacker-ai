import gradio as gr

# Sample product data
products = [
    {"name": "iPhone 15", "price": 80000},
    {"name": "MacBook Air", "price": 110000},
    {"name": "Noise Smartwatch", "price": 4000},
]

# Extract just the product names for the dropdown
product_names = [p["name"] for p in products]

def get_price(product_name):
    for product in products:
        if product["name"] == product_name:
            return product["price"]
    return 0

def negotiate_price(platform, product_name, original_price, target_price, seller_type, quantity, loyal_customer):
    try:
        original_price = float(original_price)
        target_price = float(target_price)
        if loyal_customer:
            target_price *= 0.95
        if seller_type == "reseller":
            target_price *= 0.9
        if quantity > 5:
            target_price *= 0.95
        final_price = max(target_price, original_price * 0.6)
        return f"Negotiated price for {product_name} on {platform}: ₹{round(final_price, 2)}"
    except Exception as e:
        return f"Error: {str(e)}"

def autofill_price(product_name):
    return get_price(product_name)

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("🤖 **AI Price Negotiation Tool**")

    with gr.Row():
        platform_dropdown = gr.Dropdown(
            label="Select Platform",
            choices=["Amazon", "Flipkart"],
            value="Amazon"
        )
        product_dropdown = gr.ComboBox(
            label="Select Product",
            choices=product_names,
            allow_custom_value=True,
            interactive=True
        )

    with gr.Box():
        gr.Markdown("**Original Price (auto-filled or manual)**")
        original_price_input = gr.Number(value=0, label="", interactive=True)
        gr.Markdown("**Target Price**")
        target_price_input = gr.Number(value=0, label="", interactive=True)

        gr.Markdown("**Seller Type**")
        seller_type_radio = gr.Radio(choices=["retail", "reseller"], value="retail", label="Seller Type")

        gr.Markdown("**Quantity**")
        quantity_slider = gr.Slider(minimum=1, maximum=100, value=1, label="Quantity")

        loyal_customer_checkbox = gr.Checkbox(label="Loyal Customer?")

    result_output = gr.Textbox(label="Result", lines=2)

    negotiate_button = gr.Button("Negotiate 🔥")

    # Autofill price when product is selected
    product_dropdown.change(fn=autofill_price, inputs=product_dropdown, outputs=original_price_input)

    # Trigger negotiation on button click
    negotiate_button.click(
        fn=negotiate_price,
        inputs=[
            platform_dropdown,
            product_dropdown,
            original_price_input,
            target_price_input,
            seller_type_radio,
            quantity_slider,
            loyal_customer_checkbox
        ],
        outputs=result_output
    )

# Run app
demo.launch()
