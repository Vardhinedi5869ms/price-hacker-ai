# product_fetcher.py

def get_mock_products(platform: str):
    mock_products = {
        "amazon": ["Logitech Mouse", "iPhone Charger", "Study Table"],
        "flipkart": ["Redmi Phone", "Backpack", "Washing Machine"],
        "zomato": ["Pizza Combo", "Burger Meal", "Family Dinner Pack"],
        "swiggy": ["Biryani Combo", "Dessert Box", "Healthy Meal Bowl"],
        "saas": ["Canva Pro", "Notion AI", "Grammarly Premium"]
    }

    mock_prices = {
        "Logitech Mouse": 500,
        "iPhone Charger": 1200,
        "Study Table": 3000,
        "Redmi Phone": 10000,
        "Backpack": 1500,
        "Washing Machine": 25000,
        "Pizza Combo": 399,
        "Burger Meal": 299,
        "Family Dinner Pack": 799,
        "Biryani Combo": 349,
        "Dessert Box": 249,
        "Healthy Meal Bowl": 399,
        "Canva Pro": 499,
        "Notion AI": 699,
        "Grammarly Premium": 899,
    }

    products = mock_products.get(platform.lower(), [])
    return [{"name": p, "price": mock_prices.get(p, 0)} for p in products]
