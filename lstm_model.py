# ---------------------- lstm_model.py ----------------------
import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

def predict_stock_price(ticker):
    model = load_model("models/lstm_stock_model.h5")
    df = yf.download(ticker, period="90d")
    df = df[['Close']].dropna()

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df.values)
    last_60_days = scaled_data[-60:]
    input_data = np.reshape(last_60_days, (1, 60, 1))

    predicted_scaled = model.predict(input_data)
    predicted_price = scaler.inverse_transform(predicted_scaled)[0][0]
    return float(predicted_price)
