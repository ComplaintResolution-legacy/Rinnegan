import os
import Rinnegan
import unittest
import json
import codecs
from models import PasswordRecovery, Supervisor, Complaint, Complainant
import datetime

class ComplaintResourceTestCase(unittest.TestCase):
    def setUp(self):
        # Rinnegan.app.config['TESTING'] = True
        # Rinnegan.app.config['MAIL_SUPPRESS_SEND'] = True
        self.app = Rinnegan.app.test_client()
        self.mail = Rinnegan.mail
        

        self.complainant = Complainant(
            account_handle="goyal_arush",
            account_type="twitter"
        )

        self.complainant.save()

        self.supervisor = Supervisor(
            email="someone@something.com",
            password="abcd"
        )

        self.supervisor.save()

        self.complaint = Complaint(
            text="random text",
            timestamp=datetime.datetime.now(),
            status="waiting",
            complainant_id=self.complainant.id
        )

        self.complaint.save()

    def get_complaints(self, skip, limit):
        return self.app.get(
            '/v1/complaints/ofstatus/all/' + str(skip) +'/' + str(limit)
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

    def comment(self, c_id, text):
        posted_dict = {
            'text': text
        }

        return self.app.post(
            '/v1/complaints/'+c_id+'/comments',
            data=json.dumps(posted_dict),
            content_type='application/json'
        )


    def dejsonify(self, string):
        obj = json.loads(string.decode('utf-8'))
        return obj

    def test_get_complaints(self):
        rv = self.get_complaints(0,5)
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], False)

        self.login(self.supervisor.email, self.supervisor.password)
        
        rv = self.get_complaints(0,5)
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], True)

        rv = self.get_complaints(100,200)
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'],True)
        self.assertEqual(len(j['complaints']), 0)

    def test_get_complaint(self):
        rv = self.get_complaint(self.complaint.id)
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], False)

        self.login(self.supervisor.email, self.supervisor.password)
        
        rv = self.get_complaint(self.complaint.id)
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], True)

        rv = self.get_complaint("random_string")
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'],False)

    def test_set_complaint_status(self):
        rv = self.set_complaint_status(self.complaint.id, "rejected")
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], False)

        self.login(self.supervisor.email, self.supervisor.password)
        
        rv = self.set_complaint_status("randomid", "rejected")
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'],False)

        rv = self.set_complaint_status(self.complaint.id, "somestatus")
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'],False)
        
        rv = self.set_complaint_status(self.complaint.id, "rejected")
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], True)
        rv = self.get_complaint(self.complaint.id)
        j = self.dejsonify(rv.data)
        self.assertEqual(j['complaint']['status'], "rejected")

    def test_comment(self):
        comment_text = "Hey Bro!"
        rv = self.comment(self.complaint.id, comment_text)
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], False)

        self.login(self.supervisor.email, self.supervisor.password)

        rv = self.comment("randomid", comment_text)
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], False)

        rv = self.comment(self.complaint.id, comment_text)
        j = self.dejsonify(rv.data)
        self.assertEqual(j['success'], True)

        self.complaint = Complaint.get(self.complaint.id)
        latest_comment = self.complaint.get_latest_comment()
        self.assertEqual(comment_text, latest_comment.text)


    def tearDown(self):
        self.logout()
        self.supervisor.delete()
        self.complaint.delete()
        self.complainant.delete()


if __name__ == '__main__':
    unittest.main()
