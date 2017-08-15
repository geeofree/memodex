from flask import Blueprint, jsonify
from memodex.api.router_mod import Nexus
from memodex.mock.model import users

routes = Blueprint('resources', __name__, url_prefix='/api')
nexus = Nexus(routes)
users = users.data


@routes.route('/users/', defaults={ 'userID': None })
@nexus.route('/users/<int:userID>/')
def getUsers(userID):
    if userID == None:
        return users
    else:
        try:
            user = users[userID]
            return user
        except:
            return
