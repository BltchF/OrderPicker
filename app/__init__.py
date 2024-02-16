from flask import Flask, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from app.auth import bp as auth_bp
from app.bot import bp as bot_bp
from app.order import bp as order_bp

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

app.register_blueprint(auth_bp)
app.register_blueprint(bot_bp)
app.register_blueprint(order_bp)

@app.route('/')
def index():
    return redirect(url_for('auth.login'))  
# Replace 'auth.login' with the endpoint of your login view

from app.modules import store, user, order
# Import routes and models at the end to avoid circular imports