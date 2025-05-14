# ---------------------- train_lstm_model.py ----------------------
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import os

def download_data(ticker, start='2015-01-01', end='2024-12-31'):
    df = yf.download(ticker, start=start, end=end)
    df = df[['Close']]
    df.dropna(inplace=True)
    return df

def prepare_data(df, time_steps=60):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df)

    x, y = [], []
    for i in range(time_steps, len(scaled)):
        x.append(scaled[i-time_steps:i, 0])
        y.append(scaled[i, 0])

    x, y = np.array(x), np.array(y)
    x = x.reshape((x.shape[0], x.shape[1], 1))
    return x, y, scaler

def train_lstm_model(ticker='AAPL'):
    df = download_data(ticker)
    x, y, scaler = prepare_data(df)

    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x, y, epochs=20, batch_size=32)

    os.makedirs("models", exist_ok=True)
    model.save("models/lstm_stock_model.h5")
    print("\u2705 Model trained and saved at models/lstm_stock_model.h5")

if __name__ == "__main__":
    train_lstm_model()