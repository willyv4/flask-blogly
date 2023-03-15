"""Models for Blogly."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()


class User(db.Model):
    """Users model"""

    __tablename__ = "users"

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(
    ), default='https://th.bing.com/th?id=OIP.UYefmuqvYGCqQqZN9xaW8QHaGp&w=263&h=236&c=8&rs=1&qlt=90&o=6&dpr=2&pid=3.1&rm=2')

    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name} >"


class Post(db.Model):
    """Post model"""

    __tablename__ = "posts"

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    title = Column(db.String(), nullable=False)
    content = Column(db.String(), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
