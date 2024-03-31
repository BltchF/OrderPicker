from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
from app.models import Order, Store, User, Menu, Addition, OrderItem, OrderAddition
from collections import defaultdict
from datetime import datetime, timedelta
import json
from app.extensions import db

bp = Blueprint('order', __name__)


@bp.route('/index')
def index():
    message = request.args.get('message', "")
    # Check if a user is in the session
    if 'user_id' not in session:
        # No user in the session, redirect to login page
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        # User not found, redirect to login page
        return redirect(url_for('auth.login'))

    try:
        # Get stores with their descriptions.
        stores = Store.query.with_entities(Store.name, Store.description).all()
    except Exception as e:
        # Log the error and redirect to an error page
        print(e)
        return redirect(url_for('error_page'))

    # Render the index template with the orders and stores
    return render_template('index.html', stores=stores, username=user.name, message=message)

from flask import jsonify

@bp.route('/order')
def order():
    store_name = request.args.get('store')
    if not store_name:
        return redirect(url_for('order.index'))

    try:
        # Get the store id
        store = Store.query.filter_by(name=store_name).first()
        if not store:
            message = f"Store {store_name} not found"
            return redirect(url_for('index', message=message))

    except Exception as e:
        # Log the error and redirect to an error page
        print(e)
        return redirect(url_for('error_page'))

    return render_template('order.html', store=store)

@bp.route('/api/menus')
def get_menus():
    store_name = request.args.get('store')
    if not store_name:
        return jsonify({'error': 'Store name is required'}), 400

    def menu_to_dict(menu):
        return {
            'item_id': menu.item_id,
            'item_name': menu.item_name,
            'category': menu.category,
            'price': str(menu.price),
        }

    try:
        # Get the store id
        store = Store.query.filter_by(name=store_name).first()
        if not store:
            return jsonify({'error': f'Store {store_name} not found'}), 404

        menus = Menu.query.filter_by(store_id=store.id).all()
        menus_by_category = defaultdict(list)
        for menu in menus:
            menus_by_category[menu.category].append(menu_to_dict(menu))

        # Convert the defaultdict to a list of dictionaries
        categories = [{'category': category, 'items': items} for category, items in menus_by_category.items()]

    except Exception as e:
        # Log the error and return an error response
        print(e)
        return jsonify({'error': 'An error occurred while fetching the menus'}), 500

    return jsonify(categories)

# used by AddonPopup to get the addons for a menu item
@bp.route('/api/addons')
def get_addons():
    item_id = request.args.get('item_id', type=int)
    if item_id is None:
        return jsonify({'error': 'Missing item_id parameter'}), 400
    # TODO: 修改Addition model上menu_id的問題
    try: # 後面的menu_id是指Menu資料表的item_id-->或有誤導之嫌
        additions = Addition.query.filter_by(menu_id=item_id).all()
        additions_data = [{'id': addition.id, 'add_name': addition.add_name, 'add_price': str(addition.add_price)} for addition in additions]
    except Exception as e:
        # Log the error and return an error response
        print(e)
        return jsonify({'error': 'An error occurred while fetching the addons'}), 500
    
    return jsonify(additions_data)









