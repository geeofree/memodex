from flask import Blueprint, request, jsonify

from server.webapp import auth_token
from server.model  import User

import jwt, bcrypt, datetime, pytz

resource = Blueprint('token', __name__)


@resource.route('/token/validate', methods=["GET"])
def validate_token():
    """ Route for validating a users current access token """
    token = auth_token.get_token()
    valid_token, token_status = auth_token.valid_token(token)

    if token:
        if valid_token and token_status == 200:
            return jsonify({ 'status': 409, 'status_message': 'Already signed in.' })

        if not valid_token and token_status == 400:
            return jsonify({ 'status': token_status, 'status_message': 'Invalid Token.' })

        if not valid_token and token_status == 401:
            return jsonify({ 'status': token_status, 'status_message': 'Token has expired.' })
    else:
        return jsonify({ 'status': 404, 'status_message': 'No token found' })


@resource.route('/token', methods=["POST"])
def create_token():
    """ Route for creating access tokens on valid authentications """

    data = request.get_json()
    req_username = data.get('username')
    req_password = data.get('password')

    # Check if request information is incomplete
    if not req_username or not req_password:
        return jsonify({ 'status': 400, 'status_message': 'Incomplete request information on authentication.' })

    user = User.query.filter_by(username=req_username).first()

    # Check if requested user is invalid
    if not user:
        return jsonify({ 'status': 404, 'status_message': 'User does not exist' })

    # Convert given client password and requested User password to byte code for bcrypt.checkpw()
    byte_req_pass = bytes(req_password, 'utf-8')
    byte_user_pass = bytes(user.password, 'utf-8')

    # Check if the request password matches the requested user's password
    if bcrypt.checkpw(byte_req_pass, byte_user_pass):

        datetime_now = datetime.datetime.now(tz=pytz.UTC)
        expiration_date = datetime_now + datetime.timedelta(minutes=1)

        payload = {
            'sub': user.public_id,
            'iat': datetime_now,
            'exp': expiration_date
        }

        token = auth_token.encode(payload)
        return jsonify({ 'status': 200, 'status_message': 'Authentication success', 'token': token })
    else:
        return jsonify({ 'status': 400, 'status_message': 'Username or password does not match' })
