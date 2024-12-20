import psycopg2
import pandas as pd

def connect_to_db(database_name, user, password, host, port):
    """
    Establishes a connection to the PostgreSQL database.
    """
    conn = psycopg2.connect(
        dbname=database_name,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return conn

def fetch_data(query, conn):
    """
    Fetches data from the database using the provided SQL query.
    """
    try:
        return pd.read_sql_query(query, conn)
    except Exception as e:
        print("Error while fetching data:", e)
        return None

if __name__ == "__main__":
    # Database connection details
    database_name = "xdr_database"
    user = "postgres"
    password = "3277"
    host = "localhost"
    port = "5432"

    # Establish connection
    conn = connect_to_db(database_name, user, password, host, port)
    
    # Adjust query (fix table name or check if schema is needed)
    query = 'SELECT * FROM "xdr_data";'  # Make sure the table name is correct or adjust schema
    
    # Fetch data
    data = fetch_data(query, conn)
    
    # Save to CSV if data exists
    if data is not None and not data.empty:
        data.to_csv("xdr_data.csv", index=False)
    else:
        print("No data fetched. CSV file was not saved.")
    
    # Close the connection
    conn.close()
