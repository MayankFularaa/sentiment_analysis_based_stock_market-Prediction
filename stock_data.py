import yfinance as yf

def get_last_60_days_data(ticker):
    # Fetch stock data from yfinance
    stock = yf.Ticker(ticker)
    data = stock.history(period="60d")  # Last 60 days

    if data.empty:
        return None

    return [{
        "date": row.name.strftime('%Y-%m-%d'),
        "open": row['Open'],
        "high": row['High'],
        "low": row['Low'],
        "close": row['Close'],
        "volume": row['Volume']
    } for index, row in data.iterrows()]

def get_price_yfinance(ticker):
    # Fetch current price from yfinance
    stock = yf.Ticker(ticker)
    price = stock.history(period="1d")['Close'].iloc[0]
    return price

def get_stock_history(ticker):
    data = get_last_60_days_data(ticker)
    if not data:
        return {"dates": [], "prices": [], "ohlc": [], "volumes": []}

    # Keep data in ascending order (from oldest to newest)
    # Simply don't reverse the data to keep it as is

    dates = [d['date'] for d in data]
    prices = [d['close'] for d in data]
    ohlc = [{
        't': d['date'],
        'o': d['open'],
        'h': d['high'],
        'l': d['low'],
        'c': d['close']
    } for d in data]
    volumes = [d['volume'] for d in data]

    return {
        "dates": dates,
        "prices": prices,
        "ohlc": ohlc,
        "volumes": volumes
    }
