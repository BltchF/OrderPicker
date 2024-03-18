from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
from app.models import Order, Store, User, Menu
from collections import defaultdict
import json

bp = Blueprint('order', __name__)


@bp.route('/index')
def index():
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
    return render_template('index.html', stores=stores, username=user.name)

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

# TODO: Pending for modification😔
@bp.route('/get_addons/<item_id>')
def get_addons(item_id):
    # Query database for addons of the item
    # ...
    return jsonify(addons_data)