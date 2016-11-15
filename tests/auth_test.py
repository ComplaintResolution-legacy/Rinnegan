import os
import Rinnegan
import unittest
import json
import codecs
from models import PasswordRecovery, Supervisor

class LoginResourceTestCase(unittest.TestCase):
    def setUp(self):
        # Rinnegan.app.config['TESTING'] = True
        # Rinnegan.app.config['MAIL_SUPPRESS_SEND'] = True
        self.app = Rinnegan.app.test_client()
        self.mail = Rinnegan.mail

        self.supervisor = Supervisor(
            email="someone@something.com",
            password="abcd"
        )

        self.supervisor.save()

    def login(self, email, password):
        posted_dict = {
            'email': email,
            'password': password
        }
        return self.app.post(
            '/v1/login',
            data=json.dumps(posted_dict),
            content_type='application/json'
        )

    def logout(self):
        return self.app.post(
            '/v1/logout',
            content_type='application/json'
        )

    def change_password(self, old_password, new_password):
        posted_dict = {
            'old_password': old_password,
            'new_password': new_password
        }
        return self.app.post(
            '/v1/change_password',
            data=json.dumps(posted_dict),
            content_type='application/json'
        )

    def forgot_password_p1(self, email):
        posted_dict = {
            'email': email
        }
        return self.app.post(
            '/v1/forgot_password/p1',
            data=json.dumps(posted_dict),
            content_type='application/json'
        )    

    def forgot_password_p2(self, email, token, new_password):
        posted_dict = {
            'email': email,
            'token': token,
            'new_password': new_password
        }
        return self.app.post(
            '/v1/forgot_password/p2',
            data=json.dumps(posted_dict),
            content_type='application/json'
        )                    

    def dejsonify(self, string):
        obj = json.loads(string.decode('utf-8'))
        return obj

    def test_login_logout(self):
        rv = self.login(self.supervisor.email, self.supervisor.password)
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], True)
        rv = self.logout()
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], True)
        rv = self.login('random', 'random')
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], False)

    def test_change_password(self):
        self.login(self.supervisor.email, self.supervisor.password)
        rv = self.change_password(self.supervisor.password, 'changed_password')
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], True)

        self.logout()

        rv = self.change_password('changed_password', self.supervisor.password)
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], False)

        rv = self.login(self.supervisor.email, 'changed_password')
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], True)

        rv = self.change_password('random_string', self.supervisor.password)
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], False)

        rv = self.change_password('changed_password', self.supervisor.password)

    def test_forgot_password(self):

        with self.mail.record_messages() as outbox:
            rv = self.forgot_password_p1('random@random.com')
            j = self.dejsonify(rv.data)
            self.assertEqual(j['success'], False)

            rv = self.forgot_password_p1(self.supervisor.email)
            j = self.dejsonify(rv.data)
            self.assertEqual(j['success'], True)

            s = Supervisor.search_supervisor(self.supervisor.email)
            pr = s.get_password_recovery()
            self.assertIsNotNone(pr.token)

            self.assertEqual(len(outbox) ,1)
            assert str(pr.token) in outbox[0].body 

        rv = self.forgot_password_p2('random@gmail.com', pr.token, "abcd2")
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], False)

        rv = self.forgot_password_p2(self.supervisor.email, 122, "abcd2")
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], False)
        
        rv = self.forgot_password_p2(self.supervisor.email, pr.token, "abcd2")
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], True)

        self.login(self.supervisor.email, 'abcd2')
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], True)

        self.change_password('abcd2', self.supervisor.password)
        self.logout()

    def tearDown(self):
        self.supervisor.delete()

if __name__ == '__main__':
    unittest.main()