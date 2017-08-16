from flask import Blueprint, jsonify, request

from uuid import uuid4
import datetime

from memodex.model import db
from memodex.model import User

component = Blueprint('resources', __name__, url_prefix='/api')
db.create_all()

@component.route('/users/', methods=["GET"])
def getUsers():
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


@component.route('/users/<string:publicID>', methods=["GET"])
def getSingleUser(publicID):
    try:
        user = User.query.filter_by(public_id=publicID).first()
        user_data = {
            'public_id': user.public_id,
            'username': user.username,
            'date_created': user.date_created
        }

        return jsonify({ 'status': 200, 'status_message': 'Single user request success', 'data': user_data })
    except Exception:
        return jsonify({ 'status': 400, 'status_message': 'Invalid user request' })


@component.route('/users/', methods=["POST"])
def registerUser():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({ 'status': 400, 'status_message': 'Invalid or incomplete request data' })

    try:
        newUser = User(
            public_id=str(uuid4()),
            username=username,
            password=password,
            date_created=datetime.datetime.now()
        )
        db.session.add(newUser)
        db.session.commit()
        return jsonify({ 'status': 200, 'status_message': 'New user successfuly created' })
    except Exception:
        return jsonify({ 'status': 400, 'status_message': 'Duplicate Entry' })


@component.route('/users/<string:publicID>', methods=["PUT"])
def editUser(publicID):
    try:
        data = request.get_json()
        new_username = data.get('username')

        user = User.query.filter_by(public_id=publicID).first()
        username_before_edit = user.username

        if username_before_edit == user.username:
            return jsonify({ 'status': 400, 'status_message': 'Username value is the same as before' })

        user.username = new_username
        db.session.commit()
        res_data = { 'before_edit': username_before_edit, 'after_edit': user.username }

        return jsonify({ 'status': 200, 'status_message': 'Successfully updated user', 'data': res_data })
    except Exception as error:
        print(error)
        return jsonify({ 'status': 400, 'status_message': 'Invalid user request' })


@component.route('/users/<string:publicID>', methods=["DELETE"])
def deleteUser(publicID):
    try:
        user = User.query.filter_by(public_id=publicID).first()
        db.session.delete(user)
        db.session.commit()
        return jsonify({ 'status': 200, 'status_message': 'Successfully removed user' })
    except Exception:
        return jsonify({ 'status': 400, 'status_message': 'Invalid user request' })
