from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class Usermodeltest(TestCase):
    def setUp(self):
        # Create a new user and add it to the database
        test_user = User(first_name="Bob", last_name="Smith",
                         image_url="http://example.com/avatar.jpg")
        db.session.add(test_user)
        db.session.commit()

    def test_add_user(self):

        user = User.query.filter_by(first_name="Bob").first()

        self.assertEqual(user.last_name, 'Smith')
        self.assertEqual(user.image_url, 'http://example.com/avatar.jpg')

    def test_edit_user(self):
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
        test_user = User(first_name="John", last_name="Doe",
                         image_url="http://example.com")

        test_user2 = User(first_name="Will", last_name="V",
                          image_url="http://example2.com")

        db.session.add(test_user)
        db.session.add(test_user2)
        db.session.commit()

        users = User.query.all()
        print(users)
        self.assertEqual(len(users), 6)
