# Put your unit tests here
import unittest
from unittest.mock import patch, Mock
from datetime import datetime
import sys
sys.path.append('../')
from etl_pipeline.api_client import retrieve_data, posts_endpoint, users_endpoint
from etl_pipeline.transform_data import combine_users_posts  

class TestCombineUsersPosts(unittest.TestCase):

    @patch('api_client.retrieve_data')
    def test_combine_users_posts_success(self, mock_retrieve_data):
        # Mock the posts data
        mock_posts = [
            {'userId': 1, 'id': 1, 'title': 'Title 1', 'body': 'Short body'},
            {"userId': 2, 'id': 2, 'title': 'Title 2', 'body': 'A very lengthy body that exceeds 150 characters. This is just filler text to ensure that we have a lengthy post for our tests. Let's keep going to make it even longer!"}
        ]

        # Mock the users data
        mock_users = [
            {'id': 1, 'name': 'User One', 'username': 'user1', 'email': 'user1@example.com'},
            {'id': 2, 'name': 'User Two', 'username': 'user2', 'email': 'user2@example.com'},
        ]

        # Setup the mock return values
        mock_retrieve_data.side_effect = [mock_posts, mock_users]

        # Call the function to test
        result = combine_users_posts()

        # Expected output
        expected_result = [
            {
                'userId': 1,
                'id': 1,
                'title': 'Title 1',
                'body': 'Short body',
                'status': 'concise',
                'created_at': (datetime(1970, 1, 1) + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
                'name': 'User One',
                'username': 'user1',
                'email': 'user1@example.com',
            },
            {
                'userId': 2,
                'id': 2,
                'title': 'Title 2',
                'body': 'A very lengthy body that exceeds 150 characters. This is just filler text to ensure that we have a lengthy post for our tests. Let\'s keep going to make it even longer!',
                'status': 'lengthy',
                'created_at': (datetime(1970, 1, 1) + datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
                'name': 'User Two',
                'username': 'user2',
                'email': 'user2@example.com',
            }
        ]

        # Assert the result matches the expected output
        self.assertEqual(result, expected_result)

    @patch('api_client.retrieve_data')
    def test_no_posts_data(self, mock_retrieve_data):
        # Mock the return values to simulate no posts
        mock_retrieve_data.side_effect = [None, [{'id': 1, 'name': 'User One'}]]

        # Call the function to test
        result = combine_users_posts()

        # Assert the result is an empty list
        self.assertEqual(result, [])

    @patch('api_client.retrieve_data')
    def test_no_users_data(self, mock_retrieve_data):
        # Mock the return values to simulate no users
        mock_retrieve_data.side_effect = [[{'userId': 1, 'id': 1, 'title': 'Title 1', 'body': 'Some body'}], None]

        # Call the function to test
        result = combine_users_posts()

        # Assert the result is an empty list
        self.assertEqual(result, [])

    @patch('api_client.retrieve_data')
    def test_empty_data(self, mock_retrieve_data):
        # Mock the return values to simulate empty posts and users
        mock_retrieve_data.side_effect = [[], []]

        # Call the function to test
        result = combine_users_posts()

        # Assert the result is an empty list
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
