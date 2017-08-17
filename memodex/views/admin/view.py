from flask import Blueprint, render_template

component = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')

@component.route('/')
def index():
    return render_template('admin/index.html')
