from flask import Blueprint, render_template

component = Blueprint('home', __name__)

@component.route('/')
def index():
    return render_template('home/index.html')
