from flask_restful import Resource
from flask import session, request, render_template
from flask_mail import Message

from models import Supervisor, PasswordRecovery
from Rinnegan.common import login_required
from Rinnegan import mail


class LoginResource(Resource):
    def post(self):
        args = request.get_json()

        if ('email' not in args or
            'password' not in args):
            return {
                'success': False,
                'error': "invalid input"
            } 

        supervisor = Supervisor.search_supervisor(
            args['email']
        )

        if(supervisor is None or
            not supervisor.authenticate(args['password'])):
            return {
                'success': False,
                'error': "username or password is incorrect"
            }

        session['u_id'] = supervisor.id
        return {
            'success': True,
        }


class LogoutResource(Resource):
    def post(self):
        session.pop('u_id', None)
        return {
            'success': True
        }


class ChangePasswordResource(Resource):

    @login_required
    def post(self):
        args = request.get_json()
        if (('old_password' not in args) or
            ('new_password' not in args)):
            return {
                'success': False,
                'error': "invalid input"
            }

        supervisor = Supervisor.get(session['u_id'])
        if(supervisor.password != args['old_password']):
            return {
                "success": False,
                "error": "old_password is incorrect"
            }
        supervisor.password = args['new_password']
        supervisor.save()
        return {
            "success": True
        }


class ForgotPasswordP1Resource(Resource):
    def post(self):
        args = request.get_json()
        if('email' not in args):
            return {
                'success': False,
                'error': "invalid input"
            }

        supervisor = Supervisor.search_supervisor(args['email'])
        if(supervisor is None):
            return {
                "success": False,
                "error": "email given is invalid"
            }
        pr = supervisor.create_password_recovery()
        msg = Message(
            "Forgot Password - Complaint Resolution",
            recipients=[supervisor.email],
        )
        msg.body = 'Your Password Recovery token is: ' + str(pr.token)
        mail.send(msg)

        return {
            "success": True
        }

class ForgotPasswordP2Resource(Resource):
    def post(self):
        args = request.get_json()
        if ('email' not in args or
            'token' not in args or
            'new_password' not in args):
            return {
                'success': False,
                'error': "invalid input"
            }

        supervisor = Supervisor.searchSupervisor(args['email'])
        pr = supervisor.get_password_recovery()
        if(pr is not None):
            result = pr.recover_password(args['token'], args['new_password'])
            if(result):
                return {
                    'success': True
                }

        return {
            'success' : False,
            'error': 'invalid token'
        }
