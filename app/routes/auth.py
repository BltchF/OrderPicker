from flask import Blueprint, redirect, url_for, request, session, jsonify
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
import requests
import os
from app import db
from app.models import User
from flask import render_template
import secrets

bp = Blueprint('auth', __name__)

LINE_TOKEN_URL = 'https://api.line.me/oauth2/v2.1/token'
CHANNEL_ID = os.getenv('LINE_LOGIN_CHANNEL_ID')
CHANNEL_SECRET = os.getenv('LINE_LOGIN_CHANNEL_SECRET')
CALLBACK_URL = os.getenv('LINE_LOGIN_CALLBACK_URL')



@bp.route('/login', methods=['GET', 'POST'])
def login():
    # generating a state
    state = secrets.token_urlsafe(16)
    session['state'] = state

    line_oauth_url = f'https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id={CHANNEL_ID}&redirect_uri={CALLBACK_URL}&state={state}&scope=profile%20openid%20email'

    return render_template('login.html', line_oauth_url=line_oauth_url)

@bp.route('/auth/callback')
# Listing for set CALLBACK_URL
def callback():
    # CALLBACK_URL = request.url_root.strip('/')  # CALLBACK_URL應該要是/app/auth/callback
    code = request.args.get('code')
    state = request.args.get('state')

    # Verify the state to prevent CSRF attacks
    if state != session.get('state'):                
        return redirect(url_for('main.error'))
    
    # 這邊是要對LINE的API進行post，所以要用requests
    data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': CALLBACK_URL,
        'client_id': CHANNEL_ID,
        'client_secret': CHANNEL_SECRET
    }
    print(data)                          # debug
    response = requests.post(LINE_TOKEN_URL, data=data)

    # 這邊已完成post，下面對response進行處理
    print("Before checking status code") # debug
    if response.status_code != 200:
        print(response.json())
        return redirect(url_for('main.error'))

    access_token = response.json().get('access_token')

    try:
        profile_endpoint = 'https://api.line.me/v2/profile'
        headers = {'Authorization': f'Bearer {access_token}'}
        profile_response = requests.get(profile_endpoint, headers=headers)
        
        if profile_response.status_code != 200:
            return redirect(url_for('main.error'))
        
        profile_data = profile_response.json()

        # store the relevant user data in the database
        existing_user = User.query.filter_by(line_id=profile_data['userId']).first()
        if existing_user is None:
            new_user = User(
                line_id=profile_data['userId'],
                name=profile_data['displayName'],
                picture_url=profile_data['pictureUrl'],
                privilege='user'
            )
            db.session.add(new_user)
            db.session.commit()
            existing_user = new_user
        else:
            existing_user.name = profile_data['displayName']
            existing_user.picture_url = profile_data['pictureUrl']
            db.session.commit()

        session['user_id'] = existing_user.id
    except LineBotApiError as e:
        return redirect(url_for('main.error'))

    return redirect(url_for('order.index'))

@bp.route('/logout')
def logout():
    # Remove the user_id from the session
    session.pop('user_id', None)

    # Redirect to the login page
    return redirect(url_for('auth.login'))


# ========== Debugging Delete before deploy ==================
@bp.route('/debug')
def debug():
    return jsonify({"LINE_LOGIN_CALLBACK_URL": {CALLBACK_URL}})
