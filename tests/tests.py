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

        self.ref_ajax_cors_header_val = ('Access-Control-Allow-Origin', '*')
        with open('test_data/ResponseTests/ref_pawelsiedlecki.json') as fin:
            self.ref_resp = json.loads(fin.read())
            del self.ref_resp['citedby']
        with open('test_data/ResponseTests/ref_pawelsiedlecki_ibb.json') as fin:
            self.ref_resp_author_affiliation = json.loads(fin.read())
            del self.ref_resp_author_affiliation['citedby']
        self.ref_resp_no_record = 'No record found'

    def test_response_author(self):
        """
        Test if response is correct.
        """
        self.test_resp = json.loads(
            str(self.client.get('/author/pawelsiedlecki').data, 'utf-8'),
        )[0]
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
        )[0]
        del self.test_resp['citedby']
        self.assertDictEqual(self.ref_resp_author_affiliation, self.test_resp)

    def test_response_ajax(self):
        """
        Tests if response is correct when performing ajax request.
        """
        self.test_resp = self.client.get(
            '/author/pawelsiedlecki',
            headers=[('X-Requested-With', 'XMLHttpRequest')],
        ).headers,
        assert self.ref_ajax_cors_header_val in self.test_resp[0]._list

    def test_response_no_record(self):
        """
        Test if response is correct when no record is found.
        """
        self.test_resp = self.client.get('/author/notusexistans')
        self.assertEqual(
            self.ref_resp_no_record,
            str(
                self.test_resp.data,
                'utf-8',
            ),
        )
        self.test_resp = self.client.get(
            '/author/notusexistans/affiliation/nosuchplace',
        )
        self.assertEqual(
            self.ref_resp_no_record,
            str(
                self.test_resp.data,
                'utf-8',
            ),
        )

    def test_multiple_records(self):
        """
        Test if response is correct when multiple records are found.
        """
        self.maxDiff = None
        self.test_resp = json.loads(
            str(
                self.client.get('/author/siedlecki').data,
                'utf-8',
            ),
            encoding='utf-8',
        )
        for i in self.test_resp:
            if 'citedby' in i.keys():
                del i['citedby']
        self.assertListEqual(self.ref_resp_multiple, self.test_resp)
