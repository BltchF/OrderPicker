from flask import Flask, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = app.config['FLASK_SECRET_KEY']

    # Initialize the SQLAlchemy object
    db.init_app(app)

    # Initialize the Migrate object
    migrate = Migrate(app, db)

    # Adjusted import paths to reflect the actual location of the Blueprints
    from app.routes.auth import bp as auth_bp
    from app.routes.bot import bp as bot_bp
    from app.routes.order import bp as order_bp
    from app.routes.main import bp as main_bp
    from app.routes.order_action import bp as order_action_bp

    # Register the Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(bot_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(order_action_bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app
