import requests
import logging

# Configure logging to display error messages with timestamps
logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')

# Define the API endpoints for posts and users
posts_endpoint = 'https://jsonplaceholder.typicode.com/posts'
users_endpoint = 'https://jsonplaceholder.typicode.com/users'

def retrieve_data(url):
    """
    Retrieve data from a given URL.

    Parameters:
        url (str): The URL from which to retrieve data.

    Returns:
        data (dict or None): The JSON data retrieved from the URL, or None if an error occurred.
    """
    try:
        # Make a GET request to the specified URL
        response = requests.get(url)
        
        # Raise an exception for HTTP errors (4xx and 5xx responses)
        response.raise_for_status()

        # Parse the JSON response into a Python dictionary
        data = response.json()

    except Exception as err:
        # Handle exceptions that may occur during the request
        
        # Check if the error is a client-side error (4xx)
        if response.status_code >= 400 and response.status_code < 500:
            logging.error(f'Client side error: {response.status_code}')
        
        # Check if the error is a server-side error (5xx)
        elif response.status_code >= 500 and response.status_code < 600:
            logging.error(f'Server side error: {response.status_code}')
        
        # Handle any other kind of request error
        else:
            logging.error(f'General request error: {response.status_code}')

        # Set data to None if an error occurred
        data = None

    return data
