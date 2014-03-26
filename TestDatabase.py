import os
import unittest

from config import basedir
from app import app, db
from app.models import Post
from app.views import Post

class TestDatabase(unittest.TestCase):
    """Tests various operations that add posts to the database"""
    
    def setUp(self):
        """Setup test database"""
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """Tear down test database"""
        db.session.remove()
        db.drop_all()
        
    def create_new_post(self, author, body):
        """Mocks a command that passes in a new post to the website"""
        return self.app.post('/respond/0', data = dict(author = author, body = body), follow_redirects = True)

    def create_response_post(self, author, body, pid):
        """Mocks a command that passes in a response post to the website"""
        return self.app.post('/respond/' + str(pid), data = dict(author = author, body = body, pid = pid), follow_redirects = True)
        
    def test_new_post(self):
        """Test creating a new post"""
        self.create_new_post('Allen Qiu', 'Hello world!')
        
        post0 = db.session.query(Post).filter_by(body = 'Hello world!').first()
        post1 = db.session.query(Post).filter_by(body = 'Goodbye world!').first()
        
        self.assertTrue(post0)
        self.assertEqual(None, post1)
        self.assertEqual(post0.author, 'Allen Qiu')
        self.assertEqual(post0.pid, 0)
        
        self.create_new_post('Maia', 'Goodbye world!')
        
        post0 = db.session.query(Post).filter_by(body = 'Hello world!').first()
        post1 = db.session.query(Post).filter_by(body = 'Goodbye world!').first()
        
        self.assertTrue(post0)
        self.assertTrue(post1)
        self.assertEqual(post0.author, 'Allen Qiu')
        self.assertEqual(post1.author, 'Maia')
        self.assertEqual(post0.pid, 0)
        self.assertEqual(post1.pid, 0)
        self.assertNotEqual(post0.id, post1.id)
        
    def test_response_post(self):
        """Test creating a reply post"""
        self.create_new_post('Allen Qiu', 'What is up?')        
        self.create_response_post('Maia', 'Not much!', 1)
        
        post0 = db.session.query(Post).filter_by(body = 'What is up?').first()
        post1 = db.session.query(Post).filter_by(body = 'Not much!').first()
        
        self.assertTrue(post0)
        self.assertTrue(post1)
        self.assertEqual(post0.author, 'Allen Qiu')
        self.assertEqual(post1.author, 'Maia')
        self.assertEqual(post0.pid, 0)
        self.assertEqual(post1.pid, 1)
        self.assertNotEqual(post0.id, post1.id)
        
    def test_illegal_post(self):
        """Test creating a post with one or more fields left blank"""
        self.create_new_post('Anonymous', '')        
        post0 = db.session.query(Post).filter_by(body = '').first()
        self.assertEqual(None, post0)
        
        self.create_new_post('', 'We are Anonymous!')        
        post0 = db.session.query(Post).filter_by(body = 'We are Anonymous!').first()
        self.assertEqual(None, post0)
        
    def test_censored_post(self):
        """Test to see that certain posts are censored"""
        self.create_new_post('Anonymous', 'Fuck off!')        
        post0 = db.session.query(Post).filter_by(body = 'fornicate off!').first()
        post1 = db.session.query(Post).filter_by(body = 'Fuck off').first()
        self.assertTrue(post0)
        self.assertEqual(None, post1)
        
        self.create_new_post('Anonymous', 'You really are an asshole, bastard!')        
        post0 = db.session.query(Post).filter_by(body = 'You really are an anushole, John Snow!').first()
        post1 = db.session.query(Post).filter_by(body = 'You really are an asshole, bastard').first()
        self.assertTrue(post0)
        self.assertEqual(None, post1)
        
        self.create_new_post('Anonymous', 'Just use a goto!')        
        post0 = db.session.query(Post).filter_by(body = 'Just use a he-who-must-not-be-named!').first()
        post1 = db.session.query(Post).filter_by(body = 'Just use a goto!').first()
        self.assertTrue(post0)
        self.assertEqual(None, post1)
        
    def test_sql_injection(self):
        """Test against basic SQL injection attacks (invalidated due to methodology of SQLAlchemy"""
        self.create_new_post('Anonymous', "1;DROP TABLE Post")        
        post0 = db.session.query(Post).filter_by(body = "1;DROP TABLE Post").first()
        self.assertTrue(post0)
        
        self.create_new_post('Anonymous', "105 or 1=1")        
        post0 = db.session.query(Post).filter_by(body = "105 or 1=1").first()
        self.assertTrue(post0)

if __name__ == '__main__':
    unittest.main()