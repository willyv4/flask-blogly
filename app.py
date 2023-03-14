"""Blogly application."""

from crypt import methods
from flask import Flask, redirect, render_template, request
from models import db, connect_db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "iluvu123"


connect_db(app)
db.create_all()


@app.route('/')
def root():
    return redirect('/users')


@app.route('/users')
def users():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/users/new')
def show_create_users():
    return render_template('create_user.html')


@app.route('/users/new', methods=['POST'])
def create_user():
    first = request.form['first_name']
    last = request.form['last_name']
    img_url = request.form['image_url']

    new_user = User(first_name=first, last_name=last, image_url=img_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """show details for user"""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    """ show edit user page"""
    return render_template('edit_user.html', user_id=user_id)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """ edit user """
    user = User.query.filter_by(id=user_id).first()

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """ delete user """
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
