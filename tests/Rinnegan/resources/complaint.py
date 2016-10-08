from flask_restful import Resource
from flask import session, request, jsonify

from Rinnegan.common import login_required
from models import Complaint

class ComplaintsResource(Resource):

    @login_required
    def get(self, skip, limit):
        complaints = Complaint.get_by_timestamp(skip, limit)
        complaints_json = []
        for complaint in complaints:
            complaint_json = {}
            complaint_json['id'] = complaint.id
            complaint_json['text'] = complaint.text
            complaint_json['timestamp'] = '{:%Y-%m-%d %H:%M:%S}'.format(complaint.timestamp)
            complaint_json['status'] = complaint.status

            complaints_json.append(complaint_json)

        result = {}
        result['complaints'] = complaints_json
        result['success'] = True
        return result


class ComplaintResource(Resource):

    @login_required
    def get(self, c_id):
        complaint = Complaint.get(c_id)
        if complaint is None:
            return {
                "success": False,
                "error": "404 Not found"
            }

        complaint_json = {}
        complaint_json['id'] = complaint.id
        complaint_json['text'] = complaint.text
        complaint_json['timestamp'] = '{:%Y-%m-%d %H:%M:%S}'.format(complaint.timestamp)
        complaint_json['status'] = complaint.status

        result = {}
        result['complaint'] = complaint_json
        result['success'] = True
        return result

class ComplaintStatusResource(Resource):

    @login_required
    def post(self, c_id):
        args = request.get_json()

        if ('status' not in args):
            return {
                'success': False,
                'error': "invalid input"
            }
        status = args['status']

        complaint = Complaint.get(c_id)
        if complaint is None:
            return {
                "success": False,
                "error": "404 Not found"
            }
        if(complaint.get_status() != 'waiting'):
            return {
                "success": False,
                "error": "The complaint status is already set"
            }

        try:
            complaint.set_status(status)
        except ValueError as e:
            return {
                "success": False,
                "error": "Invalid Status"
            }

        return {
            "success": True,
            "error": False
        }

