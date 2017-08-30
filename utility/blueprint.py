from shutil    import rmtree
from textwrap  import dedent
from functools import wraps

import traceback
import os

class ViewUtil:
    def __init__(self, view_name, is_prefixed, app_path=os.getcwd()):
        """ Creates a ViewUtil instance for creating an application view/blueprint

        Args:
            view_name::str
                - Name of the view/blueprint

            is_prefixed::bool
                - If set to True, set's the url_prefixed parameter on the view script
                options dictionary with the viwe_name

            app_path::str
                - The Flask Project's path. Should derive from app.root_path or the default

        Returns:
            A ViewUtil instance
        """

        self.view_name   = view_name
        self.is_prefixed = is_prefixed
        self.app_path    = app_path


    def create_blueprint(self):
        """ Creates the blueprint view tree structure or directory:

        📁ProjectName <-- Project path location given from self.app_path
            📁views
                📁BlueprintName
                    __init__.py
                    view.py
                    📁templates
                        📁BlueprintName
                            index.html
                    📁static
                         📁BlueprintName
        """

        # Path to ProjectName/views
        project_views_path = '%s/views' % self.app_path

        # Path to ProjectName/views/BlueprintName
        blueprint_dir = '%s/%s' % (project_views_path, self.view_name)

        # Make sure ProjectName/views is a directory path
        if os.path.isdir(project_views_path):

            # Make sure ProjectName/views/BlueprintName directory path
            # has not been created yet to avoid duplication
            if os.path.isdir(blueprint_dir):
                raise FileExistsError("<%s blueprint already exists for this project>" % self.view_name.title())

            try:
                print('<Creating %s blueprint>' % self.view_name.title())

                # Blueprint's directories
                subdirs = ['/', '/templates', '/static']

                for subdir in subdirs:
                    # /templates and /static blueprint folders should have a
                    # directory inside it with the same name as the view's to
                    # have the correct template or static folder name space
                    optdir = '/%s/' % self.view_name if subdir != subdirs[0] else ''

                    # Path structure: BlueprintDir + /Subdir + /OptionalDir/
                    view_dir = '%s%s%s' % (blueprint_dir, subdir, optdir)

                    # Recursively create blueprint directory tree
                    os.makedirs(view_dir)

                    # Create Root PyFiles: __init__ and view
                    if subdir == subdirs[0]:
                        self.create_pyinit(view_dir)
                        self.create_view(view_dir)
                    # Create Template Directory with an index.html file
                    elif subdir == subdirs[1]:
                        self.create_index_template(view_dir)

                print("<Done>")

            except:
                traceback.print_exc()
                print('<Destroying blueprint directory: %s>' % blueprint_dir)
                # Destroy created blueprint directory if something went wrong while creating it
                rmtree(blueprint_dir)
        else:
            raise NotADirectoryError("Flask project views path does not exist")


    def __filestream(filename='', iotype='w'):
        """ Decorates a method to have access to an opened file data on its parameters

        Args:
            filename::str
                - The name of the file to open or create

            iotype::str
                - The stream type when the file is opened, default is 'w' for creating

        Returns:
            A decorated function that has the streamed file data as the first argument
        """
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


    @__filestream(filename='__init__.py')
    def create_pyinit(self, file_data):
        """ Creates an __init__.py script to make the blueprint directory a python package """
        return file_data.write('')


    @__filestream(filename='view.py')
    def create_view(self, file_data):
        """ Creates a basic flask blueprint/view route script """

        url_prefix = "'/%s'" % self.view_name if self.is_prefixed else None

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

        template = dedent(view_template.format(self.view_name, url_prefix))
        return file_data.write(template)


    @__filestream(filename='index.html')
    def create_index_template(self, file_data):
        """ Creates a basic HTML template for the create blueprint/view """

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

        template = dedent(index_html_template.format(self.view_name.title()))
        return file_data.write(template)
