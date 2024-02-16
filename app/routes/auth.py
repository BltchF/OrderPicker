from flask import Blueprint, redirect, url_for, request, session
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
import requests
import os
from app import db
from app.models import User

bp = Blueprint('auth', __name__)

LINE_TOKEN_URL = 'https://api.line.me/oauth2/v2.1/token'
CALLBACK_URL = 'https://your-app-url/auth/callback'  # Replace with your app's callback URL

@bp.route('/auth/callback')
def callback():
    code = request.args.get('code')
    
    response = requests.post(LINE_TOKEN_URL, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': CALLBACK_URL,
        'client_id': os.getenv('LINE_LOGIN_CHANNEL_ID'),
        'client_secret': os.getenv('LINE_LOGIN_CHANNEL_SECRET')
    })

    if response.status_code != 200:
        return redirect(url_for('error'))

    access_token = response.json().get('access_token')

    try:
        profile = LineBotApi(access_token).get_profile()

        user = User.query.filter_by(line_id=profile.user_id).first()
        if user is None:
            user = User(line_id=profile.user_id, name=profile.display_name)
            db.session.add(user)
        else:
            user.name = profile.display_name

        db.session.commit()

        session['user_id'] = user.id
    except LineBotApiError as e:
        return redirect(url_for('error'))

    return redirect(url_for('index'))

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

def exchange_code_for_token(code):
    # Make a POST request to the LINE token endpoint
    response = requests.post(LINE_TOKEN_URL, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': CALLBACK_URL,
        'client_id': os.getenv('LINE_LOGIN_CHANNEL_ID'),
        'client_secret': os.getenv('LINE_LOGIN_CHANNEL_SECRET')
    })

    # Check the response status
    if response.status_code != 200:
        # Log the error and return None
        print(f"Error exchanging code for token: {response.status_code}, {response.text}")
        return None

    # Parse the JSON response and return the access token
    return response.json().get('access_token')

@bp.route('/logout')
def logout():
    # Remove the user_id from the session
    session.pop('user_id', None)

    # Redirect to the login page
    return redirect(url_for('auth.login'))