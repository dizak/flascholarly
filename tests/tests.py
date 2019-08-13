import unittest
import json


class ResponseTests(unittest.TestCase):
    """
    Tests of actual responses.
    """

    def setUp(self):
        """
        Set-up imports, test-client and reference values.

        Notes
        -------
        <citedby> is removed since it updates in real-life too quickly.
        """
        from flascholarly.app import app as tested_app


        self.client = tested_app.test_client()

        with open('test_data/ResponseTests/ref_pawelsiedlecki.json') as fin:
            self.ref_resp = json.loads(fin.read())
            del self.ref_resp['citedby']
        with open('test_data/ResponseTests/ref_pawelsiedlecki_ibb.json') as fin:
            self.ref_resp_author_affiliation = json.loads(fin.read())
            del self.ref_resp_author_affiliation['citedby']

    def test_response_author(self):
        """
        Test if response is correct.
        """
        self.test_resp = json.loads(
            str(self.client.get('/author/pawelsiedlecki').data, 'utf-8'),
        )
        del self.test_resp['citedby']
        self.assertDictEqual(self.ref_resp, self.test_resp)

    def test_response_author_affiliation(self):
        """
        Test if response is correct when queried for author and affiliation.
        """
        self.test_resp = json.loads(
            str(
                self.client.get('/author/pawelsiedlecki/affiliation/ibb').data,
                'utf-8',
            ),
        )
        del self.test_resp['citedby']
        self.assertDictEqual(self.ref_resp_author_affiliation, self.test_resp)
