from flask import Blueprint, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# Create a blueprint for bot routes
bp = Blueprint('bot', __name__)

# Replace with your channel access token and channel secret
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

# Message-reply mapping
message_reply_mapping = {
    "take my order": "please visit https://mm.cg",
    "help": "Send 'Take my order' to get the order link."
}

@bp.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    bp.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    received_text = event.message.text.lower()  # Convert to lowercase to standardize the keys
    reply_message = message_reply_mapping.get(received_text)

    if reply_message:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
    else:
        # Default response for unrecognized messages
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Sorry, I didn't understand that. Send 'help' for assistance.")
        )

