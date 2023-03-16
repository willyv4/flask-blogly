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

    tags = db.relationship('Tag', secondary='post_tags', backref='posts')


class Tag(db.Model):

    __tablename__ = "tags"

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    name = Column(db.String(10), nullable=False, unique=True)


class PostTag(db.Model):

    __tablename__ = "post_tags"

    post_id = Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    post = db.relationship('Post', backref=db.backref(
        "post_tags", cascade='all, delete-orphan'))
    tag = db.relationship('Tag', backref=db.backref(
        "post_tags", cascade='all, delete-orphan'))

    __table_args__ = (db.UniqueConstraint(
        'post_id', 'tag_id', name='_post_tag_uc'),)
