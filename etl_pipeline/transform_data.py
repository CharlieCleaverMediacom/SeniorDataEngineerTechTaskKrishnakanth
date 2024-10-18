from api_client import * 
from datetime import datetime, timedelta

def combine_users_posts():
    """
    Combine posts and user data into a single enriched data structure.

    Returns:
        post_enriched_data (list): A list of dictionaries, each containing post and user information.
    """
    
    # Retrieve posts and users information from the API
    posts_info = retrieve_data(posts_endpoint)
    users_info = retrieve_data(users_endpoint)

    # Define the UNIX epoch start date (January 1, 1970) for timestamp calculations
    epoch = datetime(1970, 1, 1)

    # Create a dictionary for fast lookup of users by their 'id'
    users_dict = {user['id']: user for user in users_info}

    # Remove the 'id' key from user dictionaries to avoid duplication in combined data
    for k, v in users_dict.items():
        users_dict[k].pop('id')

    # Initialize an empty list to hold the enriched post data
    post_enriched_data = []

    # Iterate through each post to enrich it with user data
    for post in posts_info:
        # Determine the status of the post based on the length of its body
        post['status'] = 'lengthy' if len(post['body']) > 150 else 'concise'

        # Calculate the 'created_at' timestamp using the post's 'id' as an offset from the epoch
        days_offset = post['id']  # Use the 'id' as the number of days
        created_at = epoch + timedelta(days=days_offset)

        # Format the created_at timestamp as a string in 'YYYY-MM-DD' format
        post['created_at'] = datetime.strftime(created_at, "%Y-%m-%d")

        # Get the user ID associated with the post
        user_id = post['userId']
        
        # If the user ID exists in the users dictionary, combine post and user data
        if user_id in users_dict:
            combined_data = {**post, **users_dict[user_id]}  # Merge the dictionaries
            
            # Append the combined data to the list of enriched posts
            post_enriched_data.append(combined_data)

    return post_enriched_data  # Return the list of enriched posts

