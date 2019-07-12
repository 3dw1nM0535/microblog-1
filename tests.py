from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Post
from config import Config

class TestConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI='sqlite://'

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app=create_app(TestConfig)
        self.app_context=self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u=User(username='john')
        u.set_password('test')
        self.assertFalse(u.validate_password('wrong_password'))
        self.assertTrue(u.validate_password('test'))

    def test_avatar(self):
        u=User(username='jane', email='jane@email.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/00ead251b1c1bb5580ed61753d896a15?d=identicon&s=128'))

    def test_follow(self):
        u1=User(username='jane', email='jane@emxample.com')
        u2=User(username='john', email='mary@example.com')

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # Create four users
        u1=User(username='jane', email='jane@email.com')
        u2=User(username='john', email='john@email.com')
        u3=User(username='mary', email='mary@email.com')
        u4=User(username='david', email='david@email.com')
        db.session.add_all([u1, u2, u3, u4])

        # Create four posts
        now=datetime.utcnow()
        post1=Post(body='Post from jane', author=u1, timestamp=now+timedelta(seconds=1))
        post2=Post(body='Post from john', author=u2, timestamp=now+timedelta(seconds=4))
        post3=Post(body='Post from mary', author=u3, timestamp=now+timedelta(seconds=3))
        post4=Post(body='Post from david', author=u4, timestamp=now+timedelta(seconds=2))
        db.session.add_all([post1, post2, post3, post4])
        db.session.commit()

        # Setup followers
        u1.follow(u2) # Jane follows John
        u1.follow(u4) # Jane follows David
        u2.follow(u3) # John follows Mary
        u3.follow(u4) # Mary follows David
        db.session.commit()

        # Check the followed posts of each user
        f1=u1.followed_posts().all()
        f2=u2.followed_posts().all()
        f3=u3.followed_posts().all()
        f4=u4.followed_posts().all()
        self.assertEqual(f1, [post2, post4, post1])
        self.assertEqual(f2, [post2, post3])
        self.assertEqual(f3, [post3, post4])
        self.assertEqual(f4, [post4])

if __name__ == '__main__':
    unittest.main(verbosity=2)
