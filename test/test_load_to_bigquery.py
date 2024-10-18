# Put your unit tests here
import unittest
from unittest.mock import patch, Mock
import psycopg2
import sys
sys.path.append('../')
from etl_pipeline.transform_data import combine_users_posts 


class TestDatabaseInsertion(unittest.TestCase):

    @patch('psycopg2.connect')
    def test_successful_data_insertion(self, mock_connect):
        # Mock the connection and cursor
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Sample data for testing
        data_list = [
            {
                'userId': 1,
                'name': 'John Doe',
                'username': 'johndoe',
                'email': 'john@example.com',
                'phone': '123-456-7890',
                'website': 'johndoe.com',
                'address': {
                    'street': '123 Elm St',
                    'suite': 'Apt 1',
                    'city': 'Somewhere',
                    'zipcode': '12345',
                    'geo': {
                        'lat': '40.7128',
                        'lng': '-74.0060'
                    }
                },
                'company': {
                    'name': 'Doe Inc',
                    'catchPhrase': 'Doing great things',
                    'bs': 'business solutions'
                },
                'id': 1,
                'title': 'Sample Post',
                'body': 'This is a sample post body.',
                'status': 'concise',
                'created_at': '1970-01-02'
            }
        ]

        # Call the function to insert data
        insert_data(data_list)

        # Assert that the connection was established
        mock_connect.assert_called_once()

        # Assert that the cursor was created
        mock_conn.cursor.assert_called_once()

        # Assert that the data was inserted into the users table
        mock_cursor.execute.assert_any_call(
            """
            INSERT INTO users (user_id, name, username, email, phone, website)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (1, 'John Doe', 'johndoe', 'john@example.com', '123-456-7890', 'johndoe.com')
        )

        # Check if commit was called
        mock_conn.commit.assert_called_once()

        # Assert that the connection and cursor are closed
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('psycopg2.connect')
    def test_insertion_error_handling(self, mock_connect):
        # Mock the connection and cursor
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Configure the cursor to raise an error during insertion
        mock_cursor.execute.side_effect = psycopg2.DatabaseError("Insertion error")

        data_list = [
            {
                'userId': 1,
                'name': 'John Doe',
                'username': 'johndoe',
                'email': 'john@example.com',
                'phone': '123-456-7890',
                'website': 'johndoe.com',
                'address': {
                    'street': '123 Elm St',
                    'suite': 'Apt 1',
                    'city': 'Somewhere',
                    'zipcode': '12345',
                    'geo': {
                        'lat': '40.7128',
                        'lng': '-74.0060'
                    }
                },
                'company': {
                    'name': 'Doe Inc',
                    'catchPhrase': 'Doing great things',
                    'bs': 'business solutions'
                },
                'id': 1,
                'title': 'Sample Post',
                'body': 'This is a sample post body.',
                'status': 'concise',
                'created_at': '1970-01-02'
            }
        ]

        with self.assertRaises(psycopg2.DatabaseError):
            insert_data(data_list)

        # Assert that the connection was established
        mock_connect.assert_called_once()

        # Assert that the cursor was created
        mock_conn.cursor.assert_called_once()

        # Check if the connection is closed in case of error
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
