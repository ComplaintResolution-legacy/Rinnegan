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


    def get_complaints(self, skip, limit):
        return self.app.get(
            '/v1/complaints/all/' + str(skip) +'/' + str(limit),
        )

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

    def dejsonify(self, string):
        obj = json.loads(string.decode('utf-8'))
        return obj

    def test_get_complaints(self):
        self.login('arushgyl@gmail.com', 'pepsi')
        rv = self.get_complaints(0,5)
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], True)
        rv = self.get_complaints(100,200)
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'],True)
        self.assertEqual(len(j['complaints']), 0)

if __name__ == '__main__':
    unittest.main()