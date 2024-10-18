from transform_data import *
import psycopg2

# Example nested data
data_list = combine_users_posts()

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="Krishna@890",port=5433
)
cur = conn.cursor()

# Insert data into the users, addresses, companies, and posts tables
def load_to_table():
    for data in data_list:
        # Insert user data into users table
        cur.execute(
            """
            INSERT INTO kk_users (user_id, name, username, email, phone, website)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (data['userId'], data['name'], data['username'], data['email'], data['phone'], data['website'])
        )
        user_id = cur.fetchone()[0]  # Get the inserted user ID

        # Insert address data into addresses table
        address = data['address']
        cur.execute(
            """
            INSERT INTO kk_addresses (street, suite, city, zipcode, geo_lat, geo_lng, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            (address['street'], address['suite'], address['city'], address['zipcode'],
            address['geo']['lat'], address['geo']['lng'], user_id)
        )

        # Insert company data into companies table
        company = data['company']
        cur.execute(
            """
            INSERT INTO kk_companies (name, catchphrase, bs, user_id)
            VALUES (%s, %s, %s, %s);
            """,
            (company['name'], company['catchPhrase'], company['bs'], user_id)
        )

        # Insert post data into posts table
        cur.execute(
            """
            INSERT INTO kk_posts (id, user_id, title, body, status, created_at)
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            (data['id'], user_id, data['title'], data['body'], data['status'],data['created_at'])
        )

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()
    print("Data inserted successfully!")
