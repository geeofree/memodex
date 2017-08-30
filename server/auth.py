from flask        import request, jsonify
from functools    import wraps
from server.model import User

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
        """ Decodes a given JSON Web Token

        Args:
            token::str
                - The encoded token string to be decoded

        Returns:
            A tuple with the status code and the decoded token if it is
            valid token OR status code and a status message if it isn't
        """

        try:
            return 200, jwt.decode(token, self.secret)
        except jwt.DecodeError:
            return 400, 'Invalid token.'
        except jwt.ExpiredSignatureError:
            return 401, 'Token has expired. Please log in again to continue.'


    def get_token(self):
        """ Returns the token from the X-Access-Token request header,
        or None if header is not specified """

        return request.headers.get('X-Access-Token')


    def valid_token(self, token):
        """ Same functionality as AuthToken.decode method, but includes
            the status of validity instead of the token response payload

        Args:
            token::str
                - The encoded token string to validate

        Returns:
            A tuple of the status code and boolean for the
            validity of the token
        """

        try:
            jwt.decode(token, self.secret)
            return 200, True
        except jwt.InvalidTokenError:
            return 400, False
        except jwt.ExpiredSignatureError:
            return 401, False


    def required(self, func):
        """ Decorator for flask routes to require a valid token when accessing the route """

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            token = self.get_token()

            if token == None:
                return jsonify({ 'status': 404, 'status_message': 'Token not found on header' })

            token_status, token_res = self.decode(token)

            if token_status >= 400:
                return jsonify({ 'status': token_status, 'status_message': token_res })

            try:
                return func(token_res, *args, **kwargs)
            except Exception as error:
                return jsonify({ 'status': 404, 'status_message': 'Token subject not found or invalid.' })

        return wrapped_func
