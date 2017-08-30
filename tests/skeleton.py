from server.webapp import app

class TestSkeleton:
    app = app
    test_client = app.test_client()
