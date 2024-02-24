from datetime import datetime
from ..extensions import db  # Assuming you've defined db in extensions.py or similar

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    picture_url = db.Column(db.String(255), nullable=True)
    line_id = db.Column(db.String(128), unique=True, nullable=False)
    privilege = db.Column(db.Enum('user', 'admin', 'teacher'), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Assuming you want to establish a relationship with the Role model through UserRole
    roles = db.relationship('Role', secondary='user_roles', back_populates='users')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    users = db.relationship('User', secondary='user_roles', back_populates='roles')

class UserRole(db.Model):
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
