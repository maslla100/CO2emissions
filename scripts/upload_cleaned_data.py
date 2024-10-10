import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

def load_cleaned_data(file_path):
    """Load cleaned CO2 emissions data from CSV."""
    try:
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully from {file_path}")
        return df
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return None

def upload_to_rds(df, table_name, db_url):
    """Upload DataFrame to AWS RDS PostgreSQL table."""
    try:
        engine = create_engine(db_url)
        with engine.connect() as connection:
            df.to_sql(table_name, connection, if_exists='append', index=False)
            print(f"Data uploaded successfully to {table_name} table.")
    except Exception as e:
        print(f"Error uploading data: {e}")

if __name__ == "__main__":
    # Path to the cleaned data
    cleaned_data_path = 'data/cleaned/co2_emissions_cleaned.csv'  # Adjust this path if necessary

    # Load the cleaned data
    df_cleaned = load_cleaned_data(cleaned_data_path)

    # Upload the data to RDS if loaded successfully
    if df_cleaned is not None:
        upload_to_rds(df_cleaned, "emissions_data", DATABASE_URL)
