from unittest import TestCase
from models import db, User, Post, connect_db
from app import app

# configure app for testing
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = True

db.drop_all()
db.create_all()


class Usermodeltest(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Create a new user and add it to the database for all tests in this class.
        """
        # Create a new user and add it to the database
        test_user = User(first_name="Bob", last_name="Smith",
                         image_url="http://example.com/avatar.jpg")
        db.session.add(test_user)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        """
        Delete all users and posts from the database after all tests in this class have run.
        """
        # Delete all users and posts from the database
        Post.query.delete()
        User.query.delete()
        db.session.commit()

    def test_add_user(self):
        """
        Test that a new user can be added to the database and its attributes are correct.
        """

        user = User.query.filter_by(first_name="Bob").first()

        self.assertEqual(user.last_name, 'Smith')
        self.assertEqual(user.image_url, 'http://example.com/avatar.jpg')

    def test_edit_user(self):
        """
        Test that an existing user can be edited and its updated attributes are correct.
        """
        # Get the user we just added from the database
        user = User.query.filter_by(first_name="Bob").first()

        # Update the user's attributes
        user.first_name = 'Jim'
        user.last_name = 'Jones'
        user.image_url = 'http://example.com/new_avatar.jpg'

        db.session.commit()

        # Get the user from the database again to make sure the changes were saved
        user2 = User.query.filter_by(first_name="Jim").first()

        # Check that the attributes were updated correctly
        self.assertEqual(user2.first_name, 'Jim')
        self.assertEqual(user2.last_name, 'Jones')
        self.assertEqual(user2.image_url, 'http://example.com/new_avatar.jpg')

    def test_delete_user(self):
        """
        Test that an existing user can be deleted from the database.
        """

        test_user = User(first_name="John", last_name="Doe",
                         image_url="http://example.com")

        db.session.add(test_user)
        db.session.commit()

        # Delete the user
        user = User.query.filter_by(id=test_user.id).first()
        db.session.delete(user)
        db.session.commit()

        # Check if the user was deleted
        user2 = User.query.filter_by(id=test_user.id).first()
        self.assertEqual(user2, None)

    def test_users(self):
        """
        Test that all users can be retrieved from the database and their count is correct.
        """

        test_user = User(first_name="John", last_name="Doe",
                         image_url="http://example.com")

        test_user2 = User(first_name="Will", last_name="V",
                          image_url="http://example2.com")

        db.session.add(test_user)
        db.session.add(test_user2)
        db.session.commit()

        users = User.query.all()

        self.assertEqual(len(users), 3)

    def test_create_post(self):
        """
        Test that new posts can be added to the database and their attributes are correct.
        """

        post = Post(title='wow', content='looky here')
        post1 = Post(title='1', content='looky 1')
        post2 = Post(title='2', content='looky 2')
        post3 = Post(title='3', content='looky 3')

        db.session.add_all([post, post1, post2, post3])
        db.session.commit()

        first = Post.query.get(1)
        all_posts = Post.query.all()

        self.assertEqual(len(all_posts), 4)

        self.assertEqual(first.title, 'wow')
        self.assertEqual(first.content, 'looky here')
        self.assertEqual(first.id, 1)

    def test_submit_users_edits(self):
        """
        Test that edits to a post can be submitted and its updated attributes are correct.
        """

        post = Post.query.get(1)

        post.title = 'TITLE'
        post.content = 'CONTENT'

        db.session.commit()

        self.assertEqual(post.title, 'TITLE')
        self.assertEqual(post.content, 'CONTENT')
        self.assertEqual(post.id, 1)

    def test_delete_posts(self):
        """
        Test that an existing post can be deleted from the database.
        """

        post = Post.query.get(2)
        db.session.delete(post)
        db.session.commit()

        posts = Post.query.all()

        self.assertEqual(len(posts), 3)
