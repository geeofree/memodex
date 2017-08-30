from utility.json  import jsonres
from server.webapp import app

import flask
import pytest


class TestJSONResponse:
    application = app
    test_client = app.test_client()

    def test_jsonres_correct_response(self):
        """ Test should equal to the correct dictionary response """

        correct_response = {
            'status': 200,
            'status_message': 'Ok',
            'token': 'foobarbaz'
        }

        with self.application.test_request_context():
            response = jsonres(200, 'Ok', token='foobarbaz').get_data(as_text=True)
            assert flask.json.loads(response) == correct_response


    def test_jsonres_invalid_status_code(self):
        """ Test should raise a ValueError when status_code parameter is not of type 'int' """

        # Test strings
        with pytest.raises(ValueError):
            jsonres('', 'testing')

        # Test dictonaries
        with pytest.raises(ValueError):
            jsonres({}, 'testing')

        # Test lists
        with pytest.raises(ValueError):
            jsonres([], 'testing')

        # Test tuples
        with pytest.raises(ValueError):
            jsonres((), 'testing')

        # Test sets
        with pytest.raises(ValueError):
            jsonres(set(), 'testing')

        # Test floats
        with pytest.raises(ValueError):
            jsonres(200.0, 'testing')


    def test_jsonres_invalid_status_message(self):
        """ Test should raise a ValueError when status_message parameter is not of type 'str' """

        # Test ints
        with pytest.raises(ValueError):
            jsonres(1, 1)

        # Test floats
        with pytest.raises(ValueError):
            jsonres(1, 1.0)

        # Test lists
        with pytest.raises(ValueError):
            jsonres(1, [])

        # Test tuples
        with pytest.raises(ValueError):
            jsonres(1, ())

        # Test sets
        with pytest.raises(ValueError):
            jsonres(1, set())

        # Test dictionaries
        with pytest.raises(ValueError):
            jsonres(1, {})
