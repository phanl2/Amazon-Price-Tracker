import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

DB_NAME = "prices.db"
PRODUCT_ID = 1

def fetch_prices(product_id):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(
        "SELECT price, timestamp FROM prices WHERE product_id = ? ORDER BY timestamp ASC",
        conn,
        params=(product_id,)
    )
    conn.close()
    # Normalize timestamps (handles both ISO and regular formats)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    return df

def predict_next_price(df):
    # Simple linear trend predictor for demo purposes
    df = df.copy()
    df["timestamp_ordinal"] = df["timestamp"].map(datetime.toordinal)
    X = df["timestamp_ordinal"].values.reshape(-1, 1)
    y = df["price"].values

    # Linear regression
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(X, y)

    # Predict for next day
    next_day = df["timestamp"].max() + timedelta(days=1)
    predicted_price = model.predict([[next_day.toordinal()]])[0]
    return next_day, predicted_price

if __name__ == "__main__":
    df = fetch_prices(PRODUCT_ID)
    next_day, predicted_price = predict_next_price(df)
    
    # Plot and save instead of showing
    plt.figure(figsize=(12,6))
    plt.plot(df["timestamp"], df["price"], marker='o', label="Historical Price")
    plt.axhline(y=predicted_price, color='r', linestyle='--', label=f"Predicted Price: ${predicted_price:.2f}")
    plt.scatter(next_day, predicted_price, color='r', zorder=5)
    plt.title("Product Price History & Predicted Price")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    # Save instead of show
    plt.savefig("price_history.png")
    print("Price history saved as price_history.png")
    print(f"Predicted price for {next_day.date()}: ${predicted_price:.2f}")
