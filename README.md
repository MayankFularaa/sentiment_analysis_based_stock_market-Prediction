## 📈 Sentiment Analysis-Based Stock Market Prediction
This project integrates real-time sentiment analysis from Twitter and financial news with LSTM-based stock price prediction, providing a comprehensive dashboard for visualizing, analyzing, and forecasting stock trends.

## 🧠 Project Overview
The goal is to enhance stock price forecasting by combining deep learning techniques with Natural Language Processing (NLP) for sentiment analysis, using both historical price data and real-time sentiment signals. The project is designed as a full-stack web application.

## 🚀 Key Features
🔄 Real-Time Stock Data: Fetched via the Alpha Vantage API.

📰 News Sentiment Analysis: Uses NewsAPI + FinBERT to analyze financial news articles.

🐦 Twitter Sentiment Analysis: Extracts real-time tweets, cleaned and analyzed using FinBERT.

📊 LSTM Price Prediction: Forecasts future prices using historical trends and sentiment-enhanced signals.

📉 Advanced Visualizations:

Line chart for predicted vs actual prices

Candlestick + Volume chart with SMA/EMA indicators

Sentiment score trends over time

Pie chart and word cloud for sentiment distribution

Exportable charts with zoom & pan support

🧠 NLP with Transformers: FinBERT fine-tuned on financial texts for better sentiment accuracy.

🌐 Flask Web App: Responsive UI using Tailwind CSS + Chart.js + dark-themed dashboard.

## 📦 Technologies Used
Backend: Python, Flask, yfinance, Alpha Vantage, NewsAPI, Tweepy

ML/DL: LSTM (Keras), Scikit-learn, FinBERT (HuggingFace Transformers)

Frontend: HTML, Tailwind CSS, Chart.js

NLP: Tokenization, Sentiment Scoring, Word Clouds

Visualization: Matplotlib, Plotly, Chart.js


## 🧪 Use Cases
Short-term trading insights

Market research for investors

Sentiment-driven price monitoring

Educational tool for financial analytics

🔐 Disclaimer
This project is for educational and research purposes only. It is not intended for real-time trading or financial advice.
