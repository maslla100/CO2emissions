import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def create_database_connection():
    """ Connect to PostgreSQL and create a database connection. """
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("Connection to PostgreSQL DB successful")
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_table(conn):
    """ Drop and create a table for storing CO2 emissions data. """
    drop_table_sql = '''
    DROP TABLE IF EXISTS emissions_data;
    '''
    
    create_table_sql = '''
    CREATE TABLE emissions_data (
        id SERIAL PRIMARY KEY,
        country_name TEXT NOT NULL,
        country_code TEXT,
        indicator_name TEXT,
        indicator_code TEXT,
        "1990" REAL,
        "1991" REAL,
        "1992" REAL,
        "1993" REAL,
        "1994" REAL,
        "1995" REAL,
        "1996" REAL,
        "1997" REAL,
        "1998" REAL,
        "1999" REAL,
        "2000" REAL,
        "2001" REAL,
        "2002" REAL,
        "2003" REAL,
        "2004" REAL,
        "2005" REAL,
        "2006" REAL,
        "2007" REAL,
        "2008" REAL,
        "2009" REAL,
        "2010" REAL,
        "2011" REAL,
        "2012" REAL,
        "2013" REAL,
        "2014" REAL,
        "2015" REAL,
        "2016" REAL,
        "2017" REAL,
        "2018" REAL,
        "2019" REAL,
        "2020" REAL
    );
    '''


    try:
        with conn.cursor() as cursor:
            cursor.execute(drop_table_sql)  # Drop the table if it exists
            cursor.execute(create_table_sql)  # Create the new table
            conn.commit()
            print("Table 'emissions_data' created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")

def close_connection(conn):
    """ Close the connection to the PostgreSQL database. """
    conn.close()
    print("Database connection closed.")

if __name__ == "__main__":
    conn = create_database_connection()
    if conn:
        create_table(conn)
        close_connection(conn)
