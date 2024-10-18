from transform_data import *
from load_to_databse import *

# This is the main script where you will orchestrate the ETL process, feel free to completely modify the files/structure as you see fit.
if __name__ == "__main__":
    print("ETL Job Started")

    # Transform phase
    combine_users_posts()

    # Load phase
    load_to_table()

    print("ETL Job Finished")