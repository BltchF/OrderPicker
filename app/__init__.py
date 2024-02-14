from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from .routes import auth, bot, order

# Initialize the database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Load the configuration
    app.config.from_object('config.Config')

    # Initialize the database with the app
    db.init_app(app)

    # Register the blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(bot.bp)
    app.register_blueprint(order.bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))  # Redirect to the login page

    return app