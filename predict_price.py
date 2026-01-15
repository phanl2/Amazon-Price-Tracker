from database import get_prices
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

product_id = int(input("Enter product ID to predict: "))

price_data = get_prices(product_id)

if len(price_data) < 2:
    print("Not enough data to predict")
else:
    df = pd.DataFrame(price_data, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["days"] = (df["timestamp"] - df["timestamp"].min()).dt.total_seconds() / 86400

    X = df["days"].values.reshape(-1,1)
    y = df["price"].values

    model = LinearRegression()
    model.fit(X, y)

    next_day = np.array([[df["days"].max() + 1]])
    predicted_price = model.predict(next_day)[0]
    print(f"Predicted price tomorrow: ${predicted_price:.2f}")
