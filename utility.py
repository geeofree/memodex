import os
from textwrap import dedent
from functools import wraps

class ViewUtil:
    def __init__(self, app_name, is_prefixed, app_path=os.getcwd()):
        self.app_name = app_name
        self.is_prefixed = is_prefixed
        self.app_path = app_path


    def create_blueprint(self):
        project_views_path = '%s/views' % self.app_path
        blueprint_dir = '%s/%s' % (project_views_path, self.app_name)

        if os.path.isdir(project_views_path):
            try:
                subdirs = ['', 'templates', 'static']

                for subdir in subdirs:
                    optdir = self.app_name if subdir != '' else ''
                    view_dir = '%s/%s/%s' % (blueprint_dir, subdir, optdir)
                    os.makedirs(view_dir)

                    if subdir == '':
                        self.create_pyinit(view_dir)
                        self.create_view(view_dir)
                    elif subdir == 'templates':
                        self.create_index_template(view_dir)

            except Exception as error:
                print(error)
        else:
            raise NotADirectoryError("Flask project views path does not exist")


    def filestream(filename='', iotype='w'):
        def decorator(func):
            @wraps(func)
            def wrapped_func(self, file_dir, *args, **kwargs):
                filepath = '%s/%s' % (file_dir, filename)

                with open(filepath, iotype) as file_data:
                    rv = func(self, file_data, *args, **kwargs)

                return rv
            return wrapped_func
        return decorator


    @filestream(filename='__init__.py')
    def create_pyinit(self, file_data):
        return file_data.write('')


    @filestream(filename='view.py')
    def create_view(self, file_data):

        url_prefix = "'/%s'" % self.app_name if self.is_prefixed else None

        view_template = """\
        from flask import Blueprint, render_template

        options = {{
            "url_prefix": {1},
            "template_folder": 'templates',
            "static_folder": 'static/{0}'
        }}

        component = Blueprint('{0}', __name__, **options)

        @component.route('/')
        def index():
            return render_template('{0}/index.html')
        """

        template = dedent(view_template.format(self.app_name, url_prefix))

        return file_data.write(template)


    @filestream(filename='index.html')
    def create_index_template(self, file_data):

        index_html_template = """\
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <meta http-equiv="X-UA-Compatible" content="ie=edge">
          <title>{0}</title>
        </head>
        <body>
          <h1>Welcome to the {0} Webpage!</h1>
        </body>
        </html>"""

        template = dedent(index_html_template.format(self.app_name.title()))

        return file_data.write(template)
