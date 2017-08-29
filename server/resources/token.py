from flask import Blueprint, request, jsonify

from server.webapp import auth_token
from server.model  import User

import jwt, bcrypt, datetime, pytz

resource = Blueprint('token', __name__)

@resource.route('/token/validate', methods=["GET"])
@auth_token.validate_client_token
def validate_token():
    """ Route for validating a users current access token """
    pass

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
