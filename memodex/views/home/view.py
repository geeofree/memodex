from flask import Blueprint, render_template

component = Blueprint('home', __name__, url_prefix=None, template_folder='templates', static_folder='static')

@component.route('/')
def index():
    return render_template('home/index.html')
