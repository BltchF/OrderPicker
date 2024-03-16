from datetime import datetime, timezone
from sqlalchemy import Enum
# relative import only works when taking current file as module
from ..extensions import db

# 啇店資料表
class Store(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(64))
    description = db.Column(db.String(255))
    menus = db.relationship('Menu', backref='store', lazy=True)

# 菜單資料表
class Menu(db.Model):
    __tablename__ = 'menus'
    item_id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    item_name = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Numeric(10, 2))
    size = db.Column(Enum('small', 'medium', 'large', name='size_enum'), nullable=False)
    category = db.Column(db.String(128), nullable=False)
    additions = db.relationship('Addition', backref='menu', lazy=True)

class Addition(db.Model):
    __tablename__ = 'additions'
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.item_id'), nullable=False)
    add_name = db.Column(db.String(128), nullable=False)
    add_price = db.Column(db.Numeric(10, 2))

# 使用者所點的訂單
class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    status = db.Column(Enum('pending', 'completed', 'cancelled', name='status_enum'), nullable=False)

# 訂單上的項目-考慮刪除中
class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.item_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    customizations = db.Column(db.JSON)