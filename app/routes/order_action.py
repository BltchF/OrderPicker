from flask import Blueprint, request, jsonify
from app.models import OrderItem, OrderAddition, Order, Menu, Addition
from app.extensions import db
from datetime import datetime, timedelta

bp = Blueprint('order_action', __name__)

# ==================Function related to Order List Operations==================
def create_order_additions(order_item_id, addons):
    for addon_id in addons:
        order_addition = OrderAddition(order_item_id=order_item_id, addition_id=addon_id)
        db.session.add(order_addition)

def delete_order_additions(order_item_id):
    OrderAddition.query.filter_by(order_item_id=order_item_id).delete()

def renew_order_additions(order_item_id, addons):
    delete_order_additions(order_item_id)
    create_order_additions(order_item_id, addons)

# =============================================================================




@bp.route('/api/selected_addons', methods=['POST'])
def post_selected_addons():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400

    order_item_id = data.get('order_item_id')
    addition_ids = data.get('addition_ids')
    if order_item_id is None or addition_ids is None:
        return jsonify({'error': 'Missing order_item_id or addition_ids parameter'}), 400

    try:
        # Assuming that an OrderItem with the given order_item_id exists
        order_item = OrderItem.query.get(order_item_id)

        if not order_item:
            return jsonify({'error': 'Order item not found'}), 404

        for addition_id in addition_ids:
            # Assuming that an Addition with the given addition_id exists
            addition = Addition.query.get(addition_id)

            if not addition:
                return jsonify({'error': f'Addition {addition_id} not found'}), 404

            # Create a new OrderAddition for each selected addition
            order_addition = OrderAddition(order_item_id=order_item.id, addition_id=addition.id)
            db.session.add(order_addition)

        db.session.commit()
    except Exception as e:
        return jsonify({'error': 'An error occurred while processing the selected addons'}), 500

    return jsonify({'success': 'Selected addons processed successfully'})





@bp.route('/api/order', methods=['POST'])
def post_order():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400

    store_id = data.get('store_id')
    items = data.get('items')
    user_id = data.get('user_id')
    if store_id is None or items is None or user_id is None:
        return jsonify({'error': 'Missing store_id, user_id or items parameter'}), 400

    # Try to find an existing order for the user that hasn't expired
    now = datetime.now(datetime.UTC)
    order = Order.query.filter(Order.user_id == user_id, Order.status == 'pending', Order.expires_at > now).first()

    # If no such order exists, create a new one
    if not order:
        order = Order(user_id=user_id, store_id=store_id, status='pending')
        db.session.add(order)
        db.session.flush()

    # Update the order's expires_at time
    order.expires_at = now + timedelta(minutes=30)

    # For each item in the order, create a new OrderItem
    for item in items:
        menu = Menu.query.get(item['item_id'])
        if not menu:
            return jsonify({'error': f"Menu item {item['item_id']} not found"}), 400

        order_item = OrderItem(order_id=order.id, menu_id=menu.id, quantity=item['quantity'])
        db.session.add(order_item)
        db.session.flush()

        # If the item has additions, create new OrderAddition objects
        if 'additions' in item:
            for addition_id in item['additions']:
                addition = Addition.query.get(addition_id)
                if addition:  # Only add the addition if it exists
                    order_addition = OrderAddition(order_item_id=order_item.id, addition_id=addition.id)
                    db.session.add(order_addition)
            db.session.flush()

    db.session.commit()

    return jsonify({'success': 'Order processed successfully'})