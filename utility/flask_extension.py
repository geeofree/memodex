from flask import Flask
import re

class FlaskApp(Flask):

    @staticmethod
    def valid_route_str(string):
        """ Checks if a string is a valid route string

        Args:
            string::str
                - A string to test/match for

        Returns:
            The string if it is a valid route string

        Else:
            Raise a ValueError if it isn't a valid route
        """

        route_str = re.match(r'^(/([a-zA-Z0-9\.]-?)+)+/?$', string)

        if route_str is not None:
            return string
        else:
            raise ValueError("Invalid route string value")

    def register_resource(self, blueprint, **options):
        """ Extends flask's register_blueprint method to use url_prefix set with the
            value from the API_ENDPOINT property on the app's config object

        Args:
            blueprint::Blueprint
                - A flask blueprint instance

            options::dict
                - A collection of keyword arguments for additional functionality on
                blueprints. Refer to Flask document for more information about this.

        Returns:
            A registered blueprint on the application with the url_prefix set to
            the given API_ENDPOINT config property on the application instance

        Else:
            raise a ValueError if the API_ENDPOINT is not given or None
        """

        api_endpoint = self.config.get('API_ENDPOINT')

        if api_endpoint == None:
            raise ValueError("Cannot register. No 'API_ENDPOINT' set on FlaskApp.config object")

        api_endpoint = self.valid_route_str(api_endpoint)
        self.register_blueprint(blueprint, url_prefix=api_endpoint, **options)
