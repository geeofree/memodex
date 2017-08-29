from flask import request, jsonify
from server.model import User
from functools import wraps
import jwt
import datetime
import time
import pytz


class AuthToken:

    def __init__(self, secret_key):
        self.secret = secret_key


    def encode(self, payload):
        """ JWT encode and return it as a string """
        token = jwt.encode(payload, self.secret)
        return token.decode('utf-8')


    def decode(self, token):
        """
        Decode given token, return decoded token if valid,
        return an error message payload otherwise
        """
        try:
            return jwt.decode(token, self.secret)
        except jwt.InvalidTokenError:
            return { 'status': 400, 'status_message': 'Invalid token request.' }
        except jwt.ExpiredSignatureError:
            return { 'status': 401, 'status_message': 'Token has expired. Please log in again to continue.' }


    def get_token(self):
        """ Returns a token from the X-Access-Token request header, or None if header is not specified """
        token = request.headers.get('X-Access-Token')
        return token


    def valid_token(self, token):
        """
        Same functionality as decode method, but returns a tuple containing
        containing the status of validity and status code
        """
        try:
            jwt.decode(token, self.secret)
            return True, 200
        except jwt.InvalidTokenError:
            return False, 400
        except jwt.ExpiredSignatureError:
            return False, 401


    def required(self, func):
        """
        Decorator for flask routes to have a valid token when accessing the route
        """
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            token = self.get_token()

            if token == None:
                return jsonify({ 'status': 404, 'status_message': 'Token not found' })

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
