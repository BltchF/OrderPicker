from flask import Flask, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from .extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize the SQLAlchemy object
    db.init_app(app)

    # Adjusted import paths to reflect the actual location of the Blueprints
    from app.routes.auth import bp as auth_bp
    from app.routes.bot import bp as bot_bp
    from app.routes.order import bp as order_bp

    # Register the Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(bot_bp)
    app.register_blueprint(order_bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app
