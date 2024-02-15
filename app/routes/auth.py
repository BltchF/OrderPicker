from flask import Blueprint, redirect, url_for, request
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from flask import render_template
import requests
import os


# Create a blueprint for auth routes
bp = Blueprint('auth', __name__)

# Your Channel ID and Channel Secret
LINE_LOGIN_CHANNEL_ID = os.getenv('LINE_LOGIN_CHANNEL_ID')
LINE_LOGIN_CHANNEL_SECRET = os.getenv('LINE_LOGIN_CHANNEL_SECRET')

# LINE's OAuth and token endpoints
LINE_OAUTH_URL = 'https://access.line.me/oauth2/v2.1/authorize'
LINE_TOKEN_URL = 'https://api.line.me/oauth2/v2.1/token'

# Your callback URL
CALLBACK_URL = url_for('callback', _external=True)

@bp.route('/login')
def login():
    # Construct the LINE OAuth URL
    line_oauth_url = f"{LINE_OAUTH_URL}?response_type=code&client_id={CHANNEL_ID}&redirect_uri={CALLBACK_URL}&state=12345abcde&scope=profile"
    return render_template('login.html', line_oauth_url=line_oauth_url)

from app.models import User

@bp.route('/auth/callback')
def callback():
    # Get the authorization code from the request
    code = request.args.get('code')
    
    # Exchange the code for an access token
    access_token = exchange_code_for_token(code)
    
    # Optionally, get the user profile using the access token
    try:
        profile = LineBotApi(access_token).get_profile()

        # Use profile information to create or update the user in your database
        user = User.query.filter_by(line_user_id=profile.user_id).first()
        if user is None:
            # Create a new user
            user = User(line_user_id=profile.user_id, name=profile.display_name)
            db.session.add(user)
        else:
            # Update the existing user
            user.name = profile.display_name

        db.session.commit()
    except LineBotApiError as e:
        # Handle error
        pass
    
    # Redirect or respond based on your application's flow
    return redirect(url_for('index'))

def exchange_code_for_token(code):
    # Make a POST request to the LINE token endpoint
    response = requests.post(LINE_TOKEN_URL, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': CALLBACK_URL,
        'client_id': LINE_LOGIN_CHANNEL_IDCHANNEL_ID,
        'client_secret': LINE_LOGIN_CHANNEL_SECRETCHANNEL_SECRET
    })

    # Parse the JSON response and return the access token
    return response.json()['access_token']