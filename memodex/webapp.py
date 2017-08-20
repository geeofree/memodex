from flask import Flask
app = Flask(__name__)
app.config.from_pyfile('config.cfg')

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from memodex.auth import AuthToken
auth_token = AuthToken(app.config['SECRET_KEY'])

from memodex.views.app import view as application
from memodex.commons   import token
from memodex.resources import users

app.register_blueprint(application.component)
app.register_blueprint(token.component)
app.register_blueprint(users.resource)
