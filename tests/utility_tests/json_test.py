from utility.json   import jsonres
from tests.skeleton import TestSkeleton

import flask
import pytest


class TestJSONResponse(TestSkeleton):

    def test_jsonres_correct_response(self):
        """ Test should equal to the correct json response

        GIVEN:
            The jsonres function with an int, string, and any keyword argument values as inputs

        WHEN:
            The function has proper inputs i.e an int, string, then any keyword arguments

        Then:
            Return value should be a JSON response derived from flask's jsonify function
        that should assert equally to the mock dictionary object 'correct_response' """


        correct_response = {
            'status': 200,
            'status_message': 'Ok',
            'token': 'foobarbaz',
            'stuff': {
                'foo': 20,
                'bar': 1.0
            }
        }

        with self.app.test_request_context():
            response = jsonres(200,
                        'Ok', token='foobarbaz',
                        stuff={'foo': 20, 'bar': 1.0}).get_data(as_text=True)
            assert flask.json.loads(response) == correct_response


    def test_jsonres_invalid_status_code(self):
        """ Test should raise a ValueError when status_code parameter is not of type 'int'

        GIVEN:
            The jsonres function with a non-int type on the very first input argument and
        an empty string for the second argument(required)

        WHEN:
            The function is given a non-int type on the first argument

        THEN:
            The function should raise a ValueError exception"""

        # Test strings on status_code
        with pytest.raises(ValueError):
            jsonres('', '')

        # Test dictonaries on status_code
        with pytest.raises(ValueError):
            jsonres({}, '')

        # Test lists on status_code
        with pytest.raises(ValueError):
            jsonres([], '')

        # Test tuples on status_code
        with pytest.raises(ValueError):
            jsonres((), '')

        # Test sets on status_code
        with pytest.raises(ValueError):
            jsonres(set(), '')

        # Test floats on status_code
        with pytest.raises(ValueError):
            jsonres(200.0, '')


    def test_jsonres_invalid_status_message(self):
        """ Test should raise a ValueError when status_message parameter is not of type 'str'

        GIVEN:
            The jsonres function with an int type on the very first input argument and
        a non-string type for the second argument

        WHEN:
            The function is given a non-string type on the second argument

        THEN:
            The function should raise a ValueError exception"""

        # Test ints on status_message
        with pytest.raises(ValueError):
            jsonres(1, 1)

        # Test floats on status_message
        with pytest.raises(ValueError):
            jsonres(1, 1.0)

        # Test lists on status_message
        with pytest.raises(ValueError):
            jsonres(1, [])

        # Test tuples on status_message
        with pytest.raises(ValueError):
            jsonres(1, ())

        # Test sets on status_message
        with pytest.raises(ValueError):
            jsonres(1, set())

        # Test dictionaries on status_message
        with pytest.raises(ValueError):
            jsonres(1, {})
