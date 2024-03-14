from flask import Blueprint, request, abort, url_for, current_app
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

# Create a blueprint for bot routes
bp = Blueprint('bot', __name__)

# Replace with your channel access token and channel secret
line_bot_api = LineBotApi(os.getenv('LINE_MESSAGING_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_MESSAGING_CHANNEL_SECRET'))


@bp.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    current_app.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_reply_mapping = get_message_reply_mapping()

    received_text = event.message.text.lower()  # Convert to lowercase to standardize the keys
    reply_message = message_reply_mapping.get(received_text)

    if reply_message:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
        current_app.logger.info(f"Sent reply message: {reply_message}")
    else:
        current_app.logger.info(f"No reply message found for: {received_text}")


# Message-reply mapping --> called by handle_message
def get_message_reply_mapping():
    login_url = url_for('auth.login', _external=True)
    return {
        "i wanna order": f"please visit {login_url}",
        "help": "Send 'Take my order' to get the order link.",
        "fuck you": "fuck you too"
        # Add more mappings here as needed
    }


