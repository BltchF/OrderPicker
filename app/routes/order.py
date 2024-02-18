from flask import Blueprint, render_template, session, request, redirect, url_for
from app.models import Order, Store

bp = Blueprint('order', __name__, url_prefix='/order')


@bp.route('/')
def index():
    # Check if a user is in the session
    if 'user_id' not in session:
        # No user in the session, redirect to login page
        return redirect(url_for('auth.login'))

    # Get all orders
    orders = Order.query.all()
    # Get stores with their descriptions and image URLs
    stores = Store.query.with_entities(Store.name, Store.description, Store.img_url).all()

    # Render the index template with the orders and stores
    return render_template('index.html', orders=orders, stores=stores)

@bp.route('/<store_name>')
def order(store_name):
    store = Store.query.filter_by(name=store_name).first()
    if store:
        menu = store.get_menu()
        return render_template('order.html', menu=menu)
    else:
        return "Store not found", 404
    
"""
this is herf links to order.html from jinja2 template
```
  <a href="order.html?store={{ store[0] }}" class="text-decoration-none">
```
so i think order.html should be modified

"""