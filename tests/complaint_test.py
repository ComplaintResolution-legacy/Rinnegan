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
        self.logout()


    def get_complaints(self, skip, limit):
        return self.app.get(
            '/v1/complaints/all/' + str(skip) +'/' + str(limit)
        )

    def get_complaint(self, c_id):
        return self.app.get(
            '/v1/complaints/' + c_id
        )

    def set_complaint_status(self, c_id, status):
        posted_dict = {
            'status': status
        }
        return self.app.post(
            '/v1/complaints/' + c_id +'/status',
            data=json.dumps(posted_dict),
            content_type='application/json'
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

    def logout(self):
        return self.app.post(
            '/v1/logout',
            content_type='application/json'
        )

    def dejsonify(self, string):
        obj = json.loads(string.decode('utf-8'))
        return obj

    def test_get_complaints(self):
        rv = self.get_complaints(0,5)
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], False)

        self.login('arushgyl@gmail.com', 'pepsi')
        
        rv = self.get_complaints(0,5)
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], True)

        rv = self.get_complaints(100,200)
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'],True)
        self.assertEqual(len(j['complaints']), 0)

    def test_get_complaint(self):
        rv = self.get_complaint("4af6ad88ead9301aca8772f55e00f8d1")
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], False)

        self.login('arushgyl@gmail.com', 'pepsi')
        
        rv = self.get_complaint("4af6ad88ead9301aca8772f55e00f8d1")
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], True)

        rv = self.get_complaint("Arush")
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'],False)

    def test_set_complaint_status(self):
        rv = self.set_complaint_status("4af6ad88ead9301aca8772f55e00f8d1", "rejected")
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], False)

        self.login('arushgyl@gmail.com', 'pepsi')
        
        rv = self.set_complaint_status("Arush", "rejected")
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'],False)

        rv = self.set_complaint_status("4af6ad88ead9301aca8772f55e00f8d1", "somestatus")
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'],False)
        
        rv = self.set_complaint_status("4af6ad88ead9301aca8772f55e00f8d1", "rejected")
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], True)
        rv = self.get_complaint("4af6ad88ead9301aca8772f55e00f8d1")
        j = self.dejsonify(rv.data)
        self.assertEqual(j['complaint']['status'], "rejected")


if __name__ == '__main__':
    unittest.main()
