from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    line_id = db.Column(db.String(255), unique=True, nullable=False)
    privilege = db.Column(db.String(255), default='user')

    def __repr__(self):
        return f'<User {self.name}>'
