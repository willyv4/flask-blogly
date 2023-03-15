"""Blogly application."""

from crypt import methods
from urllib.parse import uses_relative
from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "iluvu123"


connect_db(app)
db.create_all()


@app.route('/')
def root():
    """
    Redirects to the users page.
    """
    return redirect('/users')


@app.route('/users')
def users():
    """
    Renders the index.html template with a list of all users.
    """
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/users/new')
def show_create_users():
    """
    Renders the create_user.html template to show the form to create a new user.
    """
    return render_template('create_user.html')


@app.route('/users/new', methods=['POST'])
def create_user():
    """
    Creates a new user in the database and redirects to the users page.
    """
    first = request.form['first_name']
    last = request.form['last_name']
    img_url = request.form['image_url']

    new_user = User(first_name=first, last_name=last, image_url=img_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """
    Renders the details.html template with the details of the user with the given user_id and all their posts.
    """

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()

    return render_template('details.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    """
    Renders the edit_user.html template to show the form to edit the details of the user with the given user_id.
    """

    user = User.query.get(user_id)
    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """
    Edits the details of the user with the given user_id and redirects to the users page.
    """

    user = User.query.filter_by(id=user_id).first()

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """
    Deletes the user with the given user_id from the database and redirects to the users page.
    """

    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def show_add_user_form(user_id):
    """
    Renders the add_post.html template to show the form to add a new post for the user with the given user_id.
    """

    user = User.query.get(user_id)

    return render_template('add_post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def submit_add_user_form(user_id):
    """
    Creates a new post for the user with the given user_id and redirects to the user's details page.
    """

    user = User.query.get(user_id)

    title = request.form['title']
    content = request.form['content']
    user_id = user.id

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user.id}')


@app.route('/posts/<int:post_id>')
def show_users_post(post_id):
    """
    This route shows a specific post and the user who created it.
    """
    post = Post.query.get(post_id)
    user = User.query.get(post.user_id)

    return render_template('show_user_post.html', post=post, user=user)


@app.route('/posts/<int:post_id>/edit')
def display_edit_form(post_id):
    """
    This route allows the user to edit a specific post by displaying a form.
    """
    post = Post.query.get(post_id)
    return render_template('edit_post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def submit_users_edits(post_id):
    """
    This route updates a post with new content submitted by the user.
    """
    post = Post.query.get(post_id)
    user_id = post.user_id

    post.title = request.form['title']
    post.content = request.form['content']
    post.user_id = user_id

    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """
    This route deletes a post from the database.
    """

    post = Post.query.filter_by(id=post_id).first()
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')
