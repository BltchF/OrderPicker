from flask import Blueprint, render_template, session, request, redirect, url_for
from app.models import Order, Store, User, Menu
from collections import defaultdict

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
        menus = Menu.query.filter_by(store_id=store.id).all()
        munus_by_category = defaultdict(list)
        for menu in menus:
            munus_by_category[menu.category].append(menu)
    except Exception as e:
        # Log the error and redirect to an error page
        print(e)
        return redirect(url_for('error_page'))
    
    return render_template('order.html', store=store, menus_by_category=munus_by_category)

# ============================這邊待修改============================
@bp.route('/get_addons/<item_id>')
def get_addons(item_id):
    # Query database for addons of the item
    # ...
    return jsonify(addons_data)