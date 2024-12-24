import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def create_connection():
    """Create and return a connection to the PostgreSQL database."""
    try:
        connection = psycopg2.connect(
            host="localhost",  
            database="xdr_database", 
            user="postgres",  
            password="3277",
            port="5432"
        )
        return connection
    except Exception as e:
        print(f"Error: Unable to connect to the database: {e}")
        return None

def execute_query(query):
    """Execute a query and return the result as a pandas DataFrame."""
    connection = create_connection()
    if connection is None:
        return None

    try:
        # Using SQLAlchemy to make it easier for handling queries and results
        engine = create_engine('postgresql+psycopg2://postgres:3277@localhost/xdr_database')
        query_result = pd.read_sql(query, engine)
        return query_result
    except SQLAlchemyError as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        if connection:
            connection.close()

def fetch_xdr_data():
    """Fetch the xDR data from PostgreSQL."""
    query = """
    SELECT * FROM xdr_data;
    """
    return execute_query(query)
