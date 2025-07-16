import os
from flask import request
from flask_restful import Resource
from services.account_service import AccountService
from libs.helper import extract_remote_ip

INTERNAL_AUTH_SECRET = os.getenv('INTERNAL_AUTH_SECRET')

class ExternalAuthLoginApi(Resource):
    def post(self):
        # Security: Require internal secret header and secret must be set
        header_secret = request.headers.get('X-Internal-Auth')
        if not INTERNAL_AUTH_SECRET or not header_secret:
            return {"result": "fail", "data": "Unauthorized: Missing internal auth header " + str(INTERNAL_AUTH_SECRET) + " " + str(header_secret)}, 401
        if header_secret != INTERNAL_AUTH_SECRET:
            return {"result": "fail", "data": "Unauthorized: Internal auth header mismatch"}, 401

        email = request.headers.get('X-User-Email')

        if not email:
            return {"result": "fail", "data": "Missing external authentication header"}, 401

        # Get user
        account = AccountService.get_user_through_email(email)
        if not account:
            return {"result": "fail", "data": "User not found"}, 404

        # Issue Dify tokens/session
        token_pair = AccountService.login(account=account, ip_address=extract_remote_ip(request))
        return {"result": "success", "data": token_pair.model_dump()}