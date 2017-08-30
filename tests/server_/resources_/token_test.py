from tests.skeleton import TestSkeleton
from flask import json

class TestTokenAPIResource(TestSkeleton):


    def mock_login(username=None, password=None):
        """ Decorator for mocking login requests on the /api/token endpoint

        Args:
            username::str
                - Mock client's username

            password::str
                - Mock client's password

        Returns:
            A function that does equality assertions on the mocked
            login request against the decorated function's returned
            dictionary value
        """

        def decorator(func):
            def wrapped_func(self, *args, **kwargs):
                RESOURCE_ENDPOINT = '/api/token'
                CREDENTIALS       = json.dumps(dict(username=username, password=password))
                CONTENT_TYPE      = 'application/json'

                # Mock POST login request -> response
                login_res = self.test_client.post(RESOURCE_ENDPOINT,
                            data=CREDENTIALS, content_type=CONTENT_TYPE)

                # Convert the mock response to a dictionary
                test_res = json.loads(login_res.get_data(as_text=True))

                # Get the correct response dictionary
                correct_response = func(self, *args, **kwargs)

                # Equality assertion against responses
                assert test_res == correct_response
            return wrapped_func
        return decorator


    @mock_login()
    def test_create_token_incomplete_credentials(self):
        """ Test should return a response indicating the requesting client
            that they have sent an incomplete authentication form

        GIVEN:
            The client submits an incomplete authentication form, whether
            it is missing a username, a password or both

        WHEN:
            The client attempts to request authentication with an incomplete
            authentication form

        THEN:
            Return a JSON response with a status code of 400 and a status
            message indicating they have submitted an incomplete form
        """

        return { 'status': 400,
                 'status_message': 'Incomplete request information on authentication.' }


    @mock_login('invaliduser', 'invalidpassword')
    def test_create_token_invalid_user(self):
        """ Test should return a response indicating the requesting client
            has requested an invalid or non-existant user

        GIVEN:
            The client submits a valid form, complete with a username and password

        WHEN:
            The client attempts to request authentication with an invalid username

        THEN:
            Return a JSON response with a status code of 404 and a status
            message indicating that the user they are requesting to be
            authenticated as, does not exist
        """

        return { 'status': 404,
                 'status_message': 'User does not exist' }


    @mock_login('admin', 'thisisaninvalidpassword')
    def test_create_token_invalid_password(self):
        """ Test should return a response indicating the requesting client
            that they have sent invalid credentials for authentication

        GIVEN:
            The client submits a valid form, complete with a username and password

        WHEN:
            The client attempts to request authentication with a valid username
            but invalid password

        THEN:
            Return a JSON response with a status code of 400 and a status message
            indicating that the requesting client that they have mismatching
            authentication credentials
        """

        return { 'status': 400,
                 'status_message': 'Username or password does not match' }

    # TO DO:
    # Create mocks for these tests
    # Create test for successful authentications
