# Main Application instance
from utility.flask_extension import FlaskApp
app = FlaskApp(__name__)
app.config.from_pyfile('config.cfg')

# Database ORM instance
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# CORS Utility instance
from flask_cors import CORS
endpoint = r'%s/*' % app.config['API_ENDPOINT']
cors = CORS(app, resources=endpoint)

# AuthToken instance; Must be after DB ORM instantiation to work!
from server.auth import AuthToken
auth_token = AuthToken(app.config['SECRET_KEY'])

# Views and Resources registration
from server.views.app import view as application
from server.resources import token
from server.resources import users

app.register_blueprint(application.component)
app.register_resource(token.resource)
app.register_resource(users.resource)
