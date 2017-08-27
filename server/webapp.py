from utility.flask_extension import FlaskApp
app = FlaskApp(__name__)
app.config.from_pyfile('config.cfg')

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_cors import CORS
endpoint = r'%s/*' % app.config.get('API_ENDPOINT')
cors = CORS(app, resources=endpoint)

from server.auth import AuthToken
auth_token = AuthToken(app.config['SECRET_KEY'])

from server.views.app import view as application
from server.resources import token
from server.resources import users

app.register_blueprint(application.component)
app.register_resource(token.resource)
app.register_resource(users.resource)
