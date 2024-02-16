
"""
this is your suggestion for store.py
content in __init__.py of the project
```
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

from app import routes, models  
# Import routes and models at the end to avoid circular imports
```
so base on these information, I think the store.py should be modified
code me the correct store.py
"""
# store.py
from app import db

class Store(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # other fields...

    def get_menu(self):
        return Menu.query.filter_by(store_id=self.id).all()

class Menu(db.Model):
    __tablename__ = 'menus'

    item_id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # other fields...