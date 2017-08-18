from flask import request, jsonify
from memodex.model import User
from functools import wraps
import jwt
import datetime
import time
import pytz


class AuthToken:

    def __init__(self, secret_key):
        self.secret = secret_key

    def encode(self, payload):
        token = jwt.encode(payload, self.secret)
        return token.decode('utf-8')

    def decode(self, token):
        try:
            return jwt.decode(token, self.secret)
        except jwt.ExpiredSignatureError:
            return { 'status': 401, 'status_message': 'Token has expired. Please log in again to continue.' }
        except jwt.InvalidTokenError:
            return { 'status': 400, 'status_message': 'Invalid token request.' }

    def get_token(self):
        token = None
        token_header = 'x-access-token'

        if token_header in request.headers:
            token = request.headers[token_header]
        else:
            print('No access-token header')

        return token

    def valid_token(self, token):
        try:
            jwt.decode(token, self.secret)
            return True
        except Exception:
            return False

    def is_authorized(self, func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            authorized = False
            token = self.get_token()
            token_header = 'x-access-token'

            if token and self.valid_token(token):
                authorized = True

            print(authorized)
            return func(authorized, *args, **kwargs)
        return wrapped_func

    def required(self, func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            token = self.get_token()

            if not token:
                return jsonify({ 'status': 404, 'status_message': 'Token not found or no access-token header' })

            response = self.decode(token)
            res_status = response.get('status')

            if res_status != None and res_status >= 400:
                return jsonify(response)

            try:
                current_user = User.query.filter_by(public_id=response.get('sub'))
                return func(current_user, *args, **kwargs)
            except Exception as error:
                return jsonify({ 'status': 404, 'status_message': 'Token subject not found or invalid.' })

        return wrapped_func
