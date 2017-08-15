from flask import Flask
app = Flask(__name__)

from memodex.views import home, admin
from memodex.api import resources

app.register_blueprint(home.component)
app.register_blueprint(admin.component)
app.register_blueprint(resources.routes)
