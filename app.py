"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post, Tag, PostTag


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
    tags = Tag.query.all()

    return render_template('add_post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def submit_add_user_form(user_id):
    """
    Creates a new post for the user with the given user_id and redirects to the user's details page.
    """

    title = request.form['title']
    content = request.form['content']
    tag_names = request.form.getlist('name')

    tags = Tag.query.filter(Tag.name.in_(tag_names)).all()

    print('*********************')
    print('*********************')
    print('*********************')
    print(tags, 'near line 146')
    print('*********************')
    print('*********************')
    print('*********************')

    # create a new Post object and add it to the database session
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    # associate the new Post object with the selected Tag objects
    # Associate the post with the tags
    for tag in tags:
        post_tag = PostTag(post=new_post, tag=tag)
        db.session.add(post_tag)

    # Commit the changes to the database
    db.session.commit()

    # commit the changes to the database

    return redirect(f'/users/{user_id}')


@ app.route('/posts/<int:post_id>')
def show_users_post(post_id):
    """
    This route shows a specific post and the user who created it.
    """
    post = Post.query.get(post_id)
    user = User.query.get(post.user_id)

    # show posts
    tags = Tag.query.join(PostTag).filter(PostTag.post_id == post_id).all()
    print('******************')
    print(tags, 'near line 165')
    print('******************')

    return render_template('show_user_post.html', post=post, user=user, tags=tags)


@ app.route('/posts/<int:post_id>/edit')
def display_edit_form(post_id):
    """
    This route allows the user to edit a specific post by displaying a form.
    """
    post = Post.query.get(post_id)
    return render_template('edit_post.html', post=post)


@ app.route('/posts/<int:post_id>/edit', methods=['POST'])
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


@ app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """
    This route deletes a post from the database.
    """

    post = Post.query.filter_by(id=post_id).first()
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@ app.route('/tags')
def list_tags():
    tags = Tag.query.all()

    return render_template('tags_list.html', tags=tags)


@ app.route('/tags/<int:tag_id>')
def tags_details(tag_id):
    post_w_tag = PostTag.query.filter_by(tag_id=tag_id).all()
    tag = Tag.query.get(tag_id)

    posts_ids = [post.post_id for post in post_w_tag]
    posts = Post.query.filter(Post.id.in_(posts_ids)).all()

    return render_template('tag_detail.html', tag=tag, posts=posts)


@ app.route('/tags/new')
def add_new_tag():

    return render_template('tag_adder_form.html')


@ app.route('/tags/new', methods=['POST'])
def submit_new_tag_form():

    name = request.form['name']
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')


@ app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)

    return render_template('edit_tag.html', tag=tag)


@ app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def submit_tag_edit(tag_id):
    tag = Tag.query.get(tag_id)

    tag.name = request.form['name']
    db.session.commit()

    return redirect('/tags')


@ app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):

    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')
