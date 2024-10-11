import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
print(os.getenv("DATABASE_URL"))  # Add this to check if it's loading correctly

DATABASE_URL = os.getenv("DATABASE_URL")

def test_db_connection():
    try:
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL is not set.")
        
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        result = cursor.fetchone()
        print(f"DB connection test successful: {result}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_db_connection()
