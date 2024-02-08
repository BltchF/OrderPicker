from flask import Flask
from app.routes.bot import bot_blueprint  # Import the bot blueprint

app = Flask(__name__)

# Register the bot blueprint
app.register_blueprint(bot_blueprint, url_prefix='/bot')

if __name__ == "__main__":
    app.run(debug=True)
