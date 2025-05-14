from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from stock_data import get_price_yfinance, get_stock_history
from sentiment_analysis import get_twitter_sentiment
from news_sentiment import get_news_sentiment
from news_data import get_news_articles
from lstm_model import predict_stock_price
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from datetime import datetime
import os

# --- Flask App Setup ---
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# --- Login Manager Setup ---
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# --- Database Models ---
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    search_history = db.relationship('SearchHistory', backref='user', lazy=True)

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticker = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# --- User Loader for Flask-Login ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes ---

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('predict_page'))
        flash('Invalid credentials')
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/predict")
@login_required
def predict_page():
    return render_template("predict.html")

@app.route("/profile")
@login_required
def profile():
    history = SearchHistory.query.filter_by(user_id=current_user.id).order_by(SearchHistory.timestamp.desc()).all()
    return render_template("profile.html", user=current_user, history=history)

@app.route("/api/predict")
@login_required
def api_predict():
    ticker = request.args.get("ticker")
    time_frame = request.args.get("time_frame", "1d")
    try:
        db.session.add(SearchHistory(user_id=current_user.id, ticker=ticker))
        db.session.commit()
        predicted_price = predict_stock_price(ticker)
        return jsonify({"ticker": ticker, "predicted_price": predicted_price})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_current_stock_price")
def get_current_price():
    symbol = request.args.get("symbol", "")
    if not symbol:
        return jsonify({"error": "Missing stock symbol"}), 400
    try:
        price = get_price_yfinance(symbol)
        return jsonify({"symbol": symbol.upper(), "price": float(price)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def process_sentiment(ticker):
    try:
        twitter_score = get_twitter_sentiment(ticker)
        news_score = get_news_sentiment(ticker)
        avg_score = round((twitter_score + news_score) / 2, 2)
        return {
            "twitter_sentiment": twitter_score,
            "news_sentiment": news_score,
            "sentiment_score": avg_score,
            "positive": 1 if avg_score > 0 else 0,
            "neutral": 1 if avg_score == 0 else 0,
            "negative": 1 if avg_score < 0 else 0
        }
    except Exception as e:
        return {"error": str(e)}

@app.route("/sentiment/<ticker>")
def sentiment_path(ticker):
    result = process_sentiment(ticker)
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result)

@app.route("/history")
def history():
    ticker = request.args.get("ticker")
    if not ticker:
        return jsonify({"error": "Missing ticker parameter"}), 400
    try:
        history_data = get_stock_history(ticker)
        return jsonify({
            "ohlc": history_data["ohlc"],
            "prices": history_data["prices"],
            "dates": history_data["dates"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/news")
def get_news():
    ticker = request.args.get("ticker", "")
    news = get_news_articles(ticker)
    return jsonify({"articles": news})

# --- Database Setup ---
if __name__ == "__main__":
    if not os.path.exists("users.db"):
        with app.app_context():
            db.create_all()
    app.run(debug=True)
