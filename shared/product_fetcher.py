# shared/product_fetcher.py

def get_mock_products(platform: str):
    """Returns a list of mock products for the given platform."""
    mock_products = {
        "amazon": [
            {"name": "Study Table", "price": 1200},
            {"name": "Laptop Stand", "price": 900},
            {"name": "Desk Lamp", "price": 400}
        ],
        "flipkart": [
            {"name": "Office Chair", "price": 3000},
            {"name": "Bookshelf", "price": 2000},
            {"name": "Table Mat", "price": 150}
        ],
        "ajio": [
            {"name": "New Balance", "price": 10000},
            {"name": "Nike Air Max", "price": 12000},
            {"name": "Adidas Ultraboost", "price": 15000}
        ],
        "myntra": [
            {"name": "Puma Running Shoes", "price": 8000},
            {"name": "Reebok Classic", "price": 7000},
            {"name": "Under Armour", "price": 9000}
        ]
    }

    return mock_products.get(platform.lower(), [])
