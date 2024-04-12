from flask import Blueprint, request, jsonify
from app.models import OrderItem, OrderAddition, Order, Menu, Addition, User
from app.extensions import db
from datetime import datetime, timedelta, timezone

bp = Blueprint('order_action', __name__)


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

# ==================Function related to Order Operations=================
def validate_request(data):
    if not data:
        return False, jsonify({'error': 'No data received'}), 399, None

    store_id = data.get('store_id')
    items = data.get('items')
    user_id = data.get('user_id')
    if store_id is None or items is None or user_id is None or not isinstance(items, list):
        return False, jsonify({'error': 'Missing or invalid store_id, user_id or items parameter'}), 399, None

    for item in items:
        if not isinstance(item, dict) or 'item_id' not in item or 'quantity' not in item or not isinstance(item['quantity'], int):
            return False, jsonify({'error': 'Invalid item'}), 399, None
        additions = item.get('additions')
        if additions is not None and not isinstance(additions, list):
            return False, jsonify({'error': 'Invalid additions'}), 399, None

    return True, store_id, items, user_id

def get_or_create_order(user_id, store_id):
    order = Order.query.filter_by(user_id=user_id, store_id=store_id, status='pending').first()
    if not order:
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
        order = Order(user_id=user_id, store_id=store_id, status='pending', expires_at=expires_at)
        db.session.add(order)
        db.session.commit()
    return order

def process_items(items, order):
    for item in items:
        if not isinstance(item, dict) or 'item_id' not in item or 'quantity' not in item:
            return False, jsonify({'error': 'Invalid item'}), 400

        menu = Menu.query.get(item['item_id'])
        if not menu:
            return False, jsonify({'error': f"Menu item {item['item_id']} not found"}), 400

        order_item = OrderItem(order_id=order.order_id, menu_id=menu.item_id, quantity=item['quantity'])
        db.session.add(order_item)

        if 'additions' in item:
            for addition_id in item['additions']:
                addition = Addition.query.get(addition_id)
                if not addition:
                    return False, jsonify({'error': f"Addition {addition_id} not found"}), 400

                order_addition = OrderAddition(order_item_id=order_item.id, addition_id=addition.id)
                db.session.add(order_addition)

        # Extend the order's expiry time by 30 minutes every time a new item is added
        order.expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)

    return True, None, None

@bp.route('/api/order', methods=['POST'])
def post_order():
    data = request.get_json()

    valid, store_id, items, user_id = validate_request(data)
    if not valid:
        return store_id, items

    order = get_or_create_order(user_id, store_id)
    if not order:
        return jsonify({'error': 'Failed to get or create order'}), 500

    try:
        result = process_items(items, order)
        if not result:
            return jsonify({'error': 'Failed to process items'}), 500

        success, response, status = result
        if not success:
            return response, status

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)  # Log the exception
        return jsonify({'error': str(e)}), 500

    return jsonify({'success': 'Order processed successfully'})

# function for cart component to get the current order
@bp.route('/api/order', methods=['GET'])
def get_order():
    user_id = request.args.get('user_id')
    if user_id is None:
        return jsonify({'error': 'Missing user_id parameter'}), 400

    now = datetime.now(timezone.utc)
    order = Order.query.filter(Order.user_id == user_id, Order.status == 'pending', Order.expires_at > now).first()
    if not order:
        return jsonify({'error': 'No pending order found'}), 404

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    order_items = OrderItem.query.filter(OrderItem.order_id == order.order_id).all()
    items = []
    total_price = 0
    for order_item in order_items:
        menu = Menu.query.get(order_item.menu_id)
        additions = OrderAddition.query.filter(OrderAddition.order_item_id == order_item.id).all()
        addition_details = []
        for addition in additions:
            addition_item = Addition.query.get(addition.addition_id)
            addition_details.append({
                'name': addition_item.add_name,
                'price': addition_item.add_price
            })
            total_price += addition_item.add_price * order_item.quantity

        items.append({
            'name': menu.item_name,
            'quantity': order_item.quantity,
            'additions': addition_details
        })
        total_price += menu.price * order_item.quantity

    return jsonify({
        'user': user.name,
        'items': items,
        'total_price': total_price
    })

# function to delete an item from the order
@bp.route('/api/order/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = OrderItem.query.get(item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404

    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)  # Log the exception
        return jsonify({'error': str(e)}), 500

    return jsonify({'success': 'Item deleted successfully'})