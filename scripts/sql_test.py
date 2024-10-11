import psycopg2
import os

# Get the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

def test_db_connection():
    try:
        # Ensure DATABASE_URL is not None
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL is not set in the environment variables.")
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Execute a simple SQL statement
        cursor.execute('SELECT 1')

        # Fetch the result
        result = cursor.fetchone()
        print(f"Database connection test successful, result: {result}")

        # Close the cursor and connection
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error connecting to the database: {e}")

if __name__ == '__main__':
    test_db_connection()
