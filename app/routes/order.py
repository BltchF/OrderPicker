from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
from app.models import Order, Store, User, Menu, Addition
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

# used by AddonPopup to get the addons for a menu item
@bp.route('/api/addons')
def get_addons(item_id):
    menu_id = request.args.get('menu_id', type=int)
    if menu_id is None:
        return jsonify({'error': 'Missing item_id parameter'}), 400
    
    try:
        additions = Addition.query. filter_by(menu_id=menu_id).all()
        additions_data = [{'id': addition.id, 'add_name': addition.add_name, 'add_price': str(addition.add_price)} for addition in additions]
    except Exception as e:
        # Log the error and return an error response
        print(e)
        return jsonify({'error': 'An error occurred while fetching the addons'}), 500
    
    return jsonify(additions_data)


# used by AddonPopup to sent choice of addons to the server
# ! PROCEDING: not implemented
@bp.route('/api/selected_addons', methods=['POST'])
def post_selected_addons():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400
    
    item_id = data.get('item_id')
    addons = data.get('addons')
    if item_id is None or addons is None:
        return jsonify({'error': 'Missing item_id or addons parameter'}), 400
    try:
        # Here you should process the selected addons for the given item_id.
        # This depends on your application logic and database schema.
        # For example, you might create new OrderItemAddon objects and save them to the database.
        pass
    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred while processing the selected addons'}), 500

    return jsonify({'success': 'Selected addons processed successfully'})