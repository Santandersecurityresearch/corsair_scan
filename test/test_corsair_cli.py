from click.testing import CliRunner
import unittest
from unittest import TestCase
from corsair_scan import corsair_cli
from mock import patch

class TestCorsairScanManager(TestCase):

    def test_run_cli_scan_file_not_found(self):
        runner = CliRunner()
        result = runner.invoke(corsair_cli.run_cli_scan, ['dummytest.json'])
        self.assertEqual(result.output, "Error. File not found\n", "Error in test_run_cli_scan_file_not_found test")

    def test_run_cli_scan_malformed_json(self):
        runner = CliRunner()
        result = runner.invoke(corsair_cli.run_cli_scan, ['test/testfiles/json_test_malformed.json'])
        self.assertEqual(result.output, 'Error. The format does not appear to be correct, please review\n',
                         "Error in test_run_cli_scan_malformed test")

    @patch('corsair_scan.corsair_scan.corsair_scan')
    def test_run_cli_scan_error(self, corsair):
        runner = CliRunner()
        corsair.return_value = {'summary': 'test'}
        result = runner.invoke(corsair_cli.run_cli_scan, ['test/testfiles/json_test.json'])
        self.assertEqual(result.output, 'There was an error running corsair. Please check the input data is correct\n',
                         "Error in test_run_cli_scan_error test")

    @patch('corsair_scan.corsair_scan.corsair_scan')
    def test_run_cli_scan_report(self, corsair):
        runner = CliRunner()
        corsair.return_value = {'summary': {'misconfigured': [], 'error': []}, 'report': [{'url': 'https://example.com/', 'verb': 'GET', 'fake_origin': {'Origin': 'https://scarymonster.com', 'Access-Control-Allow-Origin': None, 'credentials': False, 'status_code': 400, 'error': False, 'misconfigured': False}, 'post-domain': {'Origin': 'https://example.com.scarymonster.com', 'Access-Control-Allow-Origin': None, 'credentials': False, 'status_code': 400, 'error': False, 'misconfigured': False}, 'sub-domain': {'Origin': 'https://scarymonster.example.com', 'Access-Control-Allow-Origin': None, 'credentials': False, 'status_code': 400, 'error': False, 'misconfigured': False}, 'pre-domain': {'Origin': 'https://.scarymonsterexample.com', 'Access-Control-Allow-Origin': None, 'credentials': False, 'status_code': 400, 'error': False, 'misconfigured': False}}]}
        result = runner.invoke(corsair_cli.run_cli_scan, ['test/testfiles/json_test.json', '-nv', '-r testreport.json'])
        self.assertEqual(result.output, 'Report generated in  testreport.json\n', 'Error in OK test')

if __name__ == '__main__':
    unittest.main()


