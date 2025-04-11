# shared/product_fetcher.py

def get_mock_products(platform):
    products = {
        "amazon": [
            {"name": "iPhone 15", "price": 80000},
            {"name": "MacBook Air", "price": 110000},
            {"name": "Noise Smartwatch", "price": 4000},
        ],
        "flipkart": [
            {"name": "Samsung Galaxy S23", "price": 75000},
            {"name": "HP Laptop", "price": 60000},
            {"name": "Mi Band 7", "price": 3000},
        ]
    }
    return products.get(platform.lower(), [])
