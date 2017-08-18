from flask import Flask
app = Flask(__name__)
app.config.from_pyfile('config.cfg')

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from memodex.auth import AuthToken
auth_token = AuthToken(app.config['SECRET_KEY'])

from memodex.views.general import view as general
from memodex.resources     import users

app.register_blueprint(general.component)
app.register_blueprint(users.resource)
