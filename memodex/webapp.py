from flask import Flask
app = Flask(__name__)

app.config.from_pyfile('config.cfg')

from memodex.views import home, admin
from memodex.resources import users

app.register_blueprint(home.component)
app.register_blueprint(admin.component)
app.register_blueprint(users.component)
