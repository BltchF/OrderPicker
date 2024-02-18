from flask import Blueprint, redirect, url_for, request, session
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
import requests
import os
from app import db
from app.models import User
from flask import render_template

bp = Blueprint('auth', __name__)

LINE_TOKEN_URL = 'https://api.line.me/oauth2/v2.1/token'

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Your login logic here

    channel_id = os.getenv('LINE_LOGIN_CHANNEL_ID')
    callback_url = os.getenv('LINE_LOGIN_CALLBACK_URL')
    state = os.getenv('LINE_LOGIN_STATE')  # Replace with your method for generating a state string

    line_oauth_url = f'https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id={channel_id}&redirect_uri={callback_url}&state={state}&scope=profile%20openid%20email'

    return render_template('login.html', line_oauth_url=line_oauth_url)

@bp.route('/auth/callback')
# Listing for set CALLBACK_URL
def callback():
    CALLBACK_URL = request.url_root.strip('/')  # listing on callback url
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

        user = user.query.filter_by(line_id=profile.user_id).first()
        if user is None:
            user = user(line_id=profile.user_id, name=profile.display_name)
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
    # Remove the user_id from the session
    session.pop('user_id', None)

    # Redirect to the login page
    return redirect(url_for('auth.login'))

