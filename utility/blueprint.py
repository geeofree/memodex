import os
import traceback
from shutil import rmtree as rmblueprint
from textwrap import dedent
from functools import wraps

class ViewUtil:
    def __init__(self, app_name, is_prefixed, app_path=os.getcwd()):
        self.app_name = app_name
        self.is_prefixed = is_prefixed
        self.app_path = app_path


    def create_blueprint(self):
        """
        Creates the blueprint directory along with the following structure:
            [[ProjectName]]
                |__[[views]]
                    |__[[BlueprintName]]
                        |__<__init__.py>
                        |__<view.py>
                        |__[[templates]]
                        |    |__[[BlueprintName]]
                        |        |__<index.html>
                        |__[[static]]
                             |__[[BlueprintName]]
        """

        project_views_path = '%s/views' % self.app_path
        blueprint_dir = '%s/%s' % (project_views_path, self.app_name)

        if os.path.isdir(project_views_path):

            if os.path.isdir(blueprint_dir):
                raise FileExistsError("<%s blueprint already exists for this project>" % self.app_name.title())

            try:
                print('<Creating %s blueprint>' % self.app_name.title())
                subdirs = ['/', '/templates', '/static']

                for subdir in subdirs:
                    # Optional directory for /templates and /static folders to add
                    # an extra directory inside it with the same name as the created
                    # blueprint's name
                    optdir = '/%s/' % self.app_name if subdir != subdirs[0] else ''
                    view_dir = '%s%s%s' % (blueprint_dir, subdir, optdir)
                    os.makedirs(view_dir)

                    # Create Root PyFiles: __init__ and view
                    if subdir == subdirs[0]:
                        self.create_pyinit(view_dir)
                        self.create_view(view_dir)
                    # Create Template Directory with an index html file
                    elif subdir == subdirs[1]:
                        self.create_index_template(view_dir)

                print("<Done>")

            except:
                traceback.print_exc()
                print('<Destroying blueprint directory: %s>' % blueprint_dir)
                # Destroy created blueprint directory if something went wrong while creating it
                rmblueprint(blueprint_dir)
        else:
            raise NotADirectoryError("Flask project views path does not exist")


    def filestream(filename='', iotype='w'):
        """ Method Decorator: for writing and creating(default) to a file """
        def decorator(func):
            @wraps(func)
            def wrapped_func(self, file_dir, *args, **kwargs):
                filepath = '%s%s' % (file_dir, filename)

                with open(filepath, iotype) as file_data:
                    print('<Creating File: %s>' % (filename))
                    rv = func(self, file_data, *args, **kwargs)

                return rv
            return wrapped_func
        return decorator


    @filestream(filename='__init__.py')
    def create_pyinit(self, file_data):
        """ Creates a __init__.py script to make the blueprint directory a python package """
        return file_data.write('')


    @filestream(filename='view.py')
    def create_view(self, file_data):
        """ Creates a basic flask blueprint view script """

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
        """ Creates a basic HTML template for the flask blueprint view """

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
