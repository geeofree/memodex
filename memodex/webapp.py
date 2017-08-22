from utility.flask_extension import FlaskApp
app = FlaskApp(__name__)
app.config.from_pyfile('config.cfg')

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from memodex.auth import AuthToken
auth_token = AuthToken(app.config['SECRET_KEY'])

from memodex.views.app import view as application
from memodex.resources import token
from memodex.resources import users

app.register_blueprint(application.component)
app.register_resource(token.resource)
app.register_resource(users.resource)
