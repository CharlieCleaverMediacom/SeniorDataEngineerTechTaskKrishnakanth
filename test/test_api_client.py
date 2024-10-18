# test/test_api_client.py

import unittest
from unittest.mock import patch, Mock
import requests
import sys

# Adjust the path according to your directory structure
sys.path.append('../')  # Adjust this as necessary
from etl_pipeline.api_client import retrieve_data  

class TestRetrieveData(unittest.TestCase):

    @patch('requests.get')
    def test_successful_request(self, mock_get):
        """Test for a successful API request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'key': 'value'}
        mock_get.return_value = mock_response

        result = retrieve_data('https://jsonplaceholder.typicode.com/posts')
        self.assertEqual(result, {'key': 'value'})  # Expecting the mock data

    @patch('requests.get')
    def test_client_side_error(self, mock_get):
        """Test for a client-side error (4xx)."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response

        result = retrieve_data('https://jsonplaceholder.typicode.com/posts')
        self.assertIsNone(result)  # Expecting None due to error

    @patch('requests.get')
    def test_server_side_error(self, mock_get):
        """Test for a server-side error (5xx)."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response

        result = retrieve_data('https://jsonplaceholder.typicode.com/posts')
        self.assertIsNone(result)  # Expecting None due to error

    @patch('requests.get')
    def test_general_request_error(self, mock_get):
        """Test for a general error (unexpected status code)."""
        mock_response = Mock()
        mock_response.status_code = 418  # Example status code
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response

        result = retrieve_data('https://jsonplaceholder.typicode.com/posts')
        self.assertIsNone(result)  # Expecting None due to error

    @patch('requests.get')
    def test_network_error(self, mock_get):
        """Test for a network error."""
        mock_get.side_effect = requests.exceptions.RequestException
        
        result = retrieve_data('https://jsonplaceholder.typicode.com/posts')
        self.assertIsNone(result)  # Expecting None on network error

if __name__ == '__main__':
    unittest.main()
