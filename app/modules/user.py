from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_user_id = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), nullable=True)
    # You can add more fields as needed

    def __repr__(self):
        return f'<User {self.username}>'
