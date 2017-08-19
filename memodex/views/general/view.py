from flask import Blueprint, render_template, make_response, request, jsonify

from memodex.webapp import auth_token
from memodex.model  import User

import jwt, bcrypt, datetime, pytz

component = Blueprint('general', __name__, url_prefix=None, template_folder='templates', static_folder='static')

@component.route('/')
def index():
    return render_template('general/index.html')


@component.route('/login/', methods=["GET"])
@auth_token.is_authorized
def login(is_validated):
    return render_template('general/login.html', is_validated=is_validated)


@component.route('/login/', methods=["POST"])
@auth_token.is_authorized
def validate_credentials(is_validated):

    if is_validated:
        return jsonify({ 'status': 303, 'status_message': 'Already signed in.' })

    data = request.get_json()
    req_username = data.get('username')
    req_password = data.get('password')

    # Check if request information is incomplete
    if not req_username or not req_password:
        return jsonify({ 'status': 400, 'status_message': 'Incomplete request information on authentication.' })

    user = User.query.filter_by(username=req_username).first()

    # Check if requested user is valid
    if not user:
        return jsonify({ 'status': 404, 'status_message': 'User does not exist' })

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
        response = jsonify({ 'status': 200, 'status_message': 'Authentication success' })
        response.set_cookie('token', value=token, httponly=True)
        return response
    else:
        return jsonify({ 'status': 400, 'status_message': 'Username or password does not match' })
