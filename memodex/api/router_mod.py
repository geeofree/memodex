from flask import jsonify

class Nexus:
    def __init__(self, flask_instance):
        self.flask_instance = flask_instance

    @property
    def Link(self):
        return self.link_class(self.flask_instance)

    @classmethod
    def link_class(cls, flask_instance):
        cls.flask_instance = flask_instance
        return cls

    def route(self, rule, **options):
        def decorator(func):
            @self.flask_instance.route(rule, **options)
            def wrapper(*args, **kwargs):
                resp_data = func(*args, **kwargs)

                if resp_data != None:
                    return jsonify({
                        'status': 200,
                        'status_message': 'success',
                        'data': resp_data
                    })
                else:
                    return jsonify({
                        'status': 404,
                        'status_message': 'resource not found'
                    })
            return wrapper
        return decorator
