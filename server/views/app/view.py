from flask import Blueprint, render_template

options = {
    "url_prefix": None,
    "template_folder": 'templates',
    "static_folder": 'static/app'
}

component = Blueprint('app', __name__, **options)

@component.route('/', defaults={ 'route_path': '' })
@component.route('/<path:route_path>/')
def index(route_path):
    return render_template('app/index.html')
