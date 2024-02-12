from flask import Flask
from .routes import auth, bot, order

def create_app():
    app = Flask(__name__)

    # Register the blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(bot.bp)
    app.register_blueprint(order.bp)

    @app.route('/<name>')
    def hello_name(name):
        return f"Hello {name}!"

    return app