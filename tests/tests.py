import unittest
import json


class ResponseTests(unittest.TestCase):
    """
    Tests of actual responses.
    """

    def setUp(self):
        """
        Set-up imports, test-client and reference values.
        """
        from flascholarly.app import app as tested_app


        self.client = tested_app.test_client()

        with open('test_data/ResponseTests/ref_pawelsiedlecki.json') as fin:
            self.ref_resp = json.loads(fin.read())

    def test_response(self):
        """
        Test if response is correct.
        """
        self.client.get('/author/pawelsiedlecki')
