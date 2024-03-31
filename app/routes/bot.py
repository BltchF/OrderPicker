from flask import Blueprint, request, abort, url_for, current_app
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os, unicodedata

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

    # Convert only ASCII characters to lowercase
    received_text = ''.join(c.lower() if unicodedata.name(c).startswith('LATIN') else c for c in event.message.text)
    reply_message = None

    for check, reply in message_reply_mapping:
        if check(received_text):
            reply_message = reply
            break

    if reply_message:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
        current_app.logger.info(f"Sent reply message: {reply_message}")



# Message-reply mapping --> called by handle_message
def get_message_reply_mapping():
    login_url = url_for('auth.login', _external=True, _scheme='https')
    return [
        (lambda message: "i wanna order" in message, f"please visit {login_url}"),
        (lambda message: "fuck you" in message, "fuck you too"),
        (lambda message: "推薦餐點" in message, "推薦你媽"),
        (lambda message: "點餐" in message, "點妳媽"),
        (lambda message: "help" in message, 
        "Available commands: \n1. i wanna order(only this works) \n2. help \n3. fuck you \n4. 推薦餐 \n5. 點餐")
        # Add more mappings here as needed
    ]


