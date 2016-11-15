import tweepy
import json

from flask import Flask
from flask_restful import Api, Resource
from flask_mail import Mail
import os

app = Flask(__name__)
api = Api(app)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_USE_SSL=True,
    MAIL_PORT=465,
    MAIL_USERNAME='complaintresolution40@gmail.com',
    MAIL_PASSWORD="complaint.resolution",
    MAIL_DEFAULT_SENDER=('Complaint Resolver', 'complaintresolution40@gmail.com')
)

mail = Mail(app)

twitter_cred = json.loads(os.environ['TWITTER_CRED'])

consumer_key = twitter_cred['consumer_key']
consumer_secret = twitter_cred['consumer_secret']
access_token = twitter_cred['access_token']
access_token_secret = twitter_cred['access_token_secret']

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
twitter_api = tweepy.API(auth)

from Rinnegan.resources import auth, complaint

api.add_resource(auth.LoginResource, '/v1/login')
api.add_resource(auth.LogoutResource, '/v1/logout')
api.add_resource(auth.ChangePasswordResource, '/v1/change_password')
api.add_resource(auth.ForgotPasswordP1Resource, '/v1/forgot_password/p1')
api.add_resource(auth.ForgotPasswordP2Resource, '/v1/forgot_password/p2')

api.add_resource(complaint.ComplaintsResource, '/v1/complaints/ofstatus/<status>/<int:skip>/<int:limit>')
api.add_resource(complaint.ComplaintStatusResource, '/v1/complaints/<c_id>/status')
api.add_resource(complaint.CommentResource, '/v1/complaints/<c_id>/comments')
api.add_resource(complaint.ComplaintResource, '/v1/complaints/<c_id>')


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'