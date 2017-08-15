from flask import Blueprint, render_template

component = Blueprint('admin', __name__, url_prefix='/admin')

@component.route('/')
def index():
    return render_template('admin/index.html')
