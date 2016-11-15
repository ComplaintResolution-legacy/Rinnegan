from flask_restful import Resource
from flask import session, request, jsonify

from Rinnegan.common import login_required
from models import Complaint, Comment
from Rinnegan import twitter_api

import datetime

class ComplaintsResource(Resource):

    @login_required
    def get(self, status, skip, limit):
        if((status != "all" and status != "resolved" and status != "rejected" and status!="waiting")):
            return {
                "success": False,
                "error": "Invalid input"
            }

        if(status == "all"):
            status = None

        complaints = Complaint.get_by_timestamp(skip, limit, status)
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
        result['comments'] = []

        comments = complaint.get_comments()
        for comment in comments:
            comment_json = {}
            comment_json['id'] = comment.id
            comment_json['text'] = comment.text
            comment_json['timestamp'] = '{:%Y-%m-%d %H:%M:%S}'.format(comment.timestamp)
            comment_json['by'] = comment.by

            result['comments'].append(comment_json)

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

        complainant = complaint.get_complainant()
        prev_comment = complaint.get_latest_comment()
        prev_post_id = complaint.id if prev_comment is None else prev_comment.id
        
        twitter_api.update_status(
            '@'+complainant.account_handle+'! Your complaint has been ' + status + '. Thanks for registering your complaint.',
            prev_post_id
        )

        return {
            "success": True,
            "error": False
        }

class CommentResource(Resource):

    @login_required
    def post(self, c_id):
        args = request.get_json()

        if('text' not in args):
            return {
                'success': False,
                'error': "invalid input"
            }

        complaint = Complaint.get(c_id)

        if(complaint is None):
            return {
                'success': False,
                'error': "complaint not found"
            }

        complainant = complaint.get_complainant()
        prev_comment = complaint.get_latest_comment()
        comment_text = args['text']

        prev_post_id = complaint.id if prev_comment is None else prev_comment.id
        s = twitter_api.update_status(
            '@'+complainant.account_handle+'!\n' + comment_text,
            prev_post_id
        )
        comment_id = s.id

        comment = Comment.create_comment(
            complaint,
            prev_comment,
            id=str(comment_id),
            text=comment_text,
            timestamp=datetime.datetime.now(),
            by='admin'
        )
        comment.save()

        complaint.latest_comment_id = comment.id
        complaint.save()

        return {
            'success': True
        }


