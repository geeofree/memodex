from flask import Blueprint, jsonify, request

from server.model  import db
from server.model  import User
from server.webapp import auth_token

import datetime
import bcrypt
import uuid

resource = Blueprint('users', __name__)

@resource.route('/users', methods=["GET"])
def get_users():
    """ Route for getting users """
    users = User.query.all()

    if users:
        users_data = []

        for user in users:
            user_data = {}
            user_data['public_id'] = user.public_id
            user_data['username'] = user.username
            user_data['date_created'] = user.date_created
            users_data.append(user_data)

        return jsonify({ 'status': 200, 'status_message': 'User list request success', 'data': users_data })
    else:
        return jsonify({ 'status': 404, 'status_message': 'No users found' })


@resource.route('/users/<string:public_id>', methods=["GET"])
@auth_token.required
def get_single_user(current_user, public_id):
    """ Route for getting a single user """

    try:
        user = User.query.filter_by(public_id=public_id).first()
        user_data = {
            'public_id': user.public_id,
            'username': user.username,
            'date_created': user.date_created
        }

        return jsonify({ 'status': 200, 'status_message': 'User request success', 'data': user_data })
    except Exception:
        return jsonify({ 'status': 404, 'status_message': 'User not found' })


@resource.route('/users', methods=["POST"])
def register_user():
    """ Route for creating a new user """

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({ 'status': 400, 'status_message': 'Invalid or incomplete request data' })

    try:
        encrypted_password = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
        newUser = User(
            public_id=str(uuid.uuid4()),
            username=username,
            password=encrypted_password,
            date_created=datetime.datetime.now()
        )
        db.session.add(newUser)
        db.session.commit()
        return jsonify({ 'status': 200, 'status_message': 'New user successfuly created' })
    except Exception as error:
        return jsonify({ 'status': 400, 'status_message': 'Duplicate Entry' })


@resource.route('/users/<string:public_id>', methods=["PUT"])
@auth_token.required
def edit_user(current_user, public_id):
    """ Route for updating a user """

    try:
        data = request.get_json()
        new_username = data.get('username')

        user = User.query.filter_by(public_id=public_id).first()
        username_before_edit = user.username

        if username_before_edit == user.username:
            return jsonify({ 'status': 400, 'status_message': 'Username value is the same as before' })

        user.username = new_username
        db.session.commit()
        res_data = { 'before_edit': username_before_edit, 'after_edit': user.username }

        return jsonify({ 'status': 200, 'status_message': 'Successfully updated user', 'data': res_data })
    except Exception as error:
        return jsonify({ 'status': 404, 'status_message': 'User not found' })


@resource.route('/users/<string:public_id>/', methods=["DELETE"])
@auth_token.required
def delete_user(current_user, public_id):
    """ Route for updating a user """

    try:
        user = User.query.filter_by(public_id=public_id).first()
        db.session.delete(user)
        db.session.commit()
        return jsonify({ 'status': 200, 'status_message': 'Successfully removed user' })
    except Exception:
        return jsonify({ 'status': 404, 'status_message': 'User not found' })
