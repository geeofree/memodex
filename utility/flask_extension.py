from flask import Flask
import re

class FlaskApp(Flask):

    @staticmethod
    def valid_route_str(string):
        """ Validates a string with the pattern /[Aa-Zz-09-(-)?]/? """
        route_str = re.match(r'^(/([a-zA-Z0-9\.]-?)+)+/?$', string)

        if route_str != None:
            return string
        else:
            raise ValueError("Invalid route string value")

    def register_resource(self, blueprint, **options):
        """ Registers a blueprint with the url_prefix set to the api_endpoint on the application config """
        api_endpoint = self.config.get('API_ENDPOINT')

        if api_endpoint == None:
            raise ValueError("Cannot register. No 'API_ENDPOINT' set on FlaskApp.config object")

        api_endpoint = self.valid_route_str(api_endpoint)
        self.register_blueprint(blueprint, url_prefix=api_endpoint, **options)
