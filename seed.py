from models import User, Post, Tag, db
from app import app

db.drop_all()
db.create_all()


user1 = User(first_name='Joe', last_name='Jenkins',
             image_url='https://th.bing.com/th/id/OIP.5gIHtsk6ZaujqpwQ7LsDogHaE7?w=302&h=200&c=7&r=0&o=5&dpr=2&pid=1.7')
user2 = User(first_name='Stepheny', last_name='Banks',
             image_url='https://th.bing.com/th/id/OIP.fSZNM1GwaMPBHf2VTn5wgAHaFL?w=219&h=180&c=7&r=0&o=5&dpr=2&pid=1.7')
user3 = User(first_name='Eric', last_name='Mckenzie',
             image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQGgYHFABvMF4C9TWy_cddKBXg-fZWnCOquoA&usqp=CAU')
user4 = User(first_name='Bob', last_name='Mills',
             image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6sXNuWO-A-Bx7TUStrmoNtMiPOLHcWOsYfw&usqp=CAU')


# Add users to the session
db.session.add_all([user1, user2, user3, user4])
db.session.commit()

# Create some tags
tag1 = Tag(name="python")
tag2 = Tag(name="flask")
tag3 = Tag(name="sqlalchemy")

# Add tags to the session
db.session.add_all([tag1, tag2, tag3])
db.session.commit()

# Create some posts
post1 = Post(title="First Post",
             content="This is my first post", user_id=1)
post2 = Post(title="Second Post",
             content="This is my second post", user_id=2)
post3 = Post(title="Third Post",
             content="This is my third post", user_id=3)

# Add posts to the session
db.session.add_all([post1, post2, post3])
db.session.commit()

# Assign tags to posts
post1.tags.append(tag1)
post1.tags.append(tag2)
post2.tags.append(tag2)
post3.tags.append(tag1)
post3.tags.append(tag3)

# Commit changes to the session
db.session.commit()
