from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Issues

class Tests(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='artur')
        u.set_password('larch')
        self.assertFalse(u.check_password('spam'))
        self.assertTrue(u.check_password('larch'))




class BasicSitesTest(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_issues_page(self):
        response = self.app.get('/issues/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_new_issue_page(self):
        response = self.app.get('/new_issue/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_users_page(self):
        response = self.app.get('/users/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_machine_page(self):
        response = self.app.get('/add_machine/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_payments_page(self):
        response = self.app.get('/payments/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_customers_page(self):
        response = self.app.get('/customers/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)