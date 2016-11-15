from flask import session

def login_required(func):

    def inner_function(*args, **kwargs):
        if('u_id' in session):
            return func(*args, **kwargs)
        else:
            return {
                'success': False,
                'error': 'Login is Required'
            }
    return inner_function