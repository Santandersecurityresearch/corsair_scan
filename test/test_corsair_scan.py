import unittest
from unittest import TestCase
from corsair_scan import corsair_scan
from mock import MagicMock


class TestCorsairScanManager(TestCase):

    def test_validate_data_wrong_url(self):
        verb = 'GET'
        url = 'htts://www.test.com'
        self.assertFalse(corsair_scan.validate_data(url, verb), ' Error in wrong url test')

    def test_validate_data_wrong_verb(self):
        verb = 'blah'
        url = 'https://www.test.com'
        self.assertFalse(corsair_scan.validate_data(url, verb), 'Error in wrong verb test')

    def test_corsair_scan_no_origin(self):
        data = []
        item = {}
        item['url'] = 'https://www.test.com'
        item['verb'] = 'GET'
        item['params'] = 'a=b'
        item['headers'] = {'header1':'value1', 'header2':'value2'}
        report = {'summary': {'misconfigured': [{'url': 'https://www.test.com', 'verb': 'GET', 'status_code': 200, 'credentials': False, 'misconfigured_test': ['fake_origin']}], 'error': []}, 'report': [{'url': 'https://www.test.com', 'verb': 'GET', 'fake_origin': {'Origin': 'https://scarymonster.com', 'Access-Control-Allow-Origin': 'https://scarymonster.com', 'credentials': False, 'status_code': 200, 'error': False, 'misconfigured': True}}]}
        data.append(item)
        corsair_scan.requests = MagicMock()
        response = MagicMock()
        response.headers = {'Access-Control-Allow-Origin' : 'https://scarymonster.com'}
        response.status_code = 200
        corsair_scan.requests.get.return_value = response
        self.assertEqual(corsair_scan.corsair_scan(data), report, 'Error in bulk - no origin')

    def test_corsair_scan_origin(self):
        data = []
        item = {}
        item['url'] = 'https://www.test.com'
        item['verb'] = 'GET'
        item['params'] = 'a=b'
        item['headers'] = {'header1':'value1', 'header2':'value2', 'Origin': 'https://scarymonster.com'}
        report = {'summary': {'misconfigured': [{'url': 'https://www.test.com', 'verb': 'GET', 'status_code': 200, 'credentials': False, 'misconfigured_test': ['fake_origin']}], 'error': []}, 'report': [{'url': 'https://www.test.com', 'verb': 'GET', 'fake_origin': {'Origin': 'https://scarymonster.com', 'Access-Control-Allow-Origin': 'https://scarymonster.com', 'credentials': False, 'status_code': 200, 'error': False, 'misconfigured': True}, 'post-domain': {'Origin': 'https://scarymonster.com.scarymonster.com', 'Access-Control-Allow-Origin': 'https://scarymonster.com', 'credentials': False, 'status_code': 200, 'error': False, 'misconfigured': False}, 'sub-domain': {'Origin': 'https://scarymonster.scarymonster.com', 'Access-Control-Allow-Origin': 'https://scarymonster.com', 'credentials': False, 'status_code': 200, 'error': False, 'misconfigured': False}, 'pre-domain': {'Origin': 'https://.scarymonsterscarymonster.com', 'Access-Control-Allow-Origin': 'https://scarymonster.com', 'credentials': False, 'status_code': 200, 'error': False, 'misconfigured': False}}]}
        data.append(item)
        corsair_scan.requests = MagicMock()
        response = MagicMock()
        response.headers = {'Access-Control-Allow-Origin' : 'https://scarymonster.com'}
        response.status_code = 200
        corsair_scan.requests.get.return_value = response
        self.assertEqual(corsair_scan.corsair_scan(data), report, 'Error in bulk - origin')

    def test_corsair_scan_401(self):
        data = []
        item = {}
        item['url'] = 'https://www.test.com'
        item['verb'] = 'GET'
        item['params'] = 'a=b'
        item['headers'] = {'header1': 'value1', 'header2': 'value2', 'Origin': 'https://scarymonster.com'}
        report = {'summary': {'misconfigured': [{'url': 'https://www.test.com', 'verb': 'GET', 'status_code': 401, 'credentials': False, 'misconfigured_test': ['fake_origin']}], 'error': [{'url': 'https://www.test.com', 'verb': 'GET', 'status_code': 401, 'credentials': False, 'misconfigured_test': ['fake_origin']}]}, 'report': [{'url': 'https://www.test.com', 'verb': 'GET', 'fake_origin': {'Origin': 'https://scarymonster.com', 'Access-Control-Allow-Origin': 'https://scarymonster.com', 'credentials': False, 'status_code': 401, 'error': True, 'misconfigured': True}, 'post-domain': {'Origin': 'https://scarymonster.com.scarymonster.com', 'Access-Control-Allow-Origin': 'https://scarymonster.com', 'credentials': False, 'status_code': 401, 'error': True, 'misconfigured': False}, 'sub-domain': {'Origin': 'https://scarymonster.scarymonster.com', 'Access-Control-Allow-Origin': 'https://scarymonster.com', 'credentials': False, 'status_code': 401, 'error': True, 'misconfigured': False}, 'pre-domain': {'Origin': 'https://.scarymonsterscarymonster.com', 'Access-Control-Allow-Origin': 'https://scarymonster.com', 'credentials': False, 'status_code': 401, 'error': True, 'misconfigured': False}}]}
        data.append(item)
        corsair_scan.requests = MagicMock()
        response = MagicMock()
        response.headers = {'Access-Control-Allow-Origin': 'https://scarymonster.com'}
        response.status_code = 401
        corsair_scan.requests.get.return_value = response
        self.assertEqual(corsair_scan.corsair_scan(data), report, 'Error in bulk - 401')

if __name__ == '__main__':
    unittest.main()