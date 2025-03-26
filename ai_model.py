import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Simulated dataset of price negotiations
data = {
    "original_price": [1000, 5000, 20000, 8000, 10000, 30000, 15000, 40000, 25000, 50000],
    "target_price": [900, 4500, 18000, 7200, 9000, 27000, 13500, 36000, 22500, 45000],
    "final_price": [950, 4700, 18500, 7500, 9200, 28000, 14000, 38000, 23500, 47000],
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Train a RandomForest model instead of LinearRegression
X = df[["original_price", "target_price"]]
y = df["final_price"]

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

def predict_price(original_price, target_price):
    """
    Predicts the best possible negotiated price using AI.
    """
    input_data = pd.DataFrame([[original_price, target_price]], columns=["original_price", "target_price"])
    predicted_price = model.predict(input_data)[0]
    return round(predicted_price, 2)
