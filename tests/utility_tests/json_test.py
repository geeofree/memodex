from utility.json import json_response
from server.webapp import app

import flask
import pytest


class TestJSONResponse:
    application = app
    test_client = app.test_client()

    def test_json_response_correct_response(self):
        """ Test should equal to the correct dictionary response """

        correct_response = {
            'status': 200,
            'status_message': 'Ok',
            'token': 'foobarbaz'
        }

        with self.application.test_request_context():
            response = json_response(200, 'Ok', token='foobarbaz').get_data(as_text=True)
            assert flask.json.loads(response) == correct_response


    def test_json_response_invalid_status_code(self):
        """ Test should raise a ValueError when status_code parameter is not of type 'int' """

        # Test strings
        with pytest.raises(ValueError):
            json_response('', 'testing')

        # Test dictonaries
        with pytest.raises(ValueError):
            json_response({}, 'testing')

        # Test lists
        with pytest.raises(ValueError):
            json_response([], 'testing')

        # Test tuples
        with pytest.raises(ValueError):
            json_response((), 'testing')

        # Test sets
        with pytest.raises(ValueError):
            json_response(set(), 'testing')

        # Test floats
        with pytest.raises(ValueError):
            json_response(200.0, 'testing')


    def test_json_response_invalid_status_message(self):
        """ Test should raise a ValueError when status_message parameter is not of type 'str' """

        # Test ints
        with pytest.raises(ValueError):
            json_response(1, 1)

        # Test floats
        with pytest.raises(ValueError):
            json_response(1, 1.0)

        # Test lists
        with pytest.raises(ValueError):
            json_response(1, [])

        # Test tuples
        with pytest.raises(ValueError):
            json_response(1, ())

        # Test sets
        with pytest.raises(ValueError):
            json_response(1, set())

        # Test dictionaries
        with pytest.raises(ValueError):
            json_response(1, {})
