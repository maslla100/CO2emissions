import pandas as pd

def load_data(file_path):
    """Load the CO2 emissions dataset."""
    try:
        df = pd.read_csv(file_path, skiprows=4)  # Adjust for file structure (skip metadata rows)
        print(f"Data loaded successfully from {file_path}")
        return df
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return None

def clean_data(df):
    """Clean and preprocess the CO2 emissions data."""
    # Remove unnamed columns and fill missing values
    df_cleaned = df.loc[:, ~df.columns.str.contains('^Unnamed')].copy()

    # Forward-fill missing values
    df_cleaned.ffill(inplace=True)
    
    # Ensure no rows with NaN remain
    df_cleaned.dropna(how='all', inplace=True)

    # Rename columns to match PostgreSQL table schema (remove spaces, lowercase, use underscores)
    df_cleaned.columns = df_cleaned.columns.str.strip().str.lower().str.replace(' ', '_')
    
    print("Data cleaning and renaming columns completed.")
    return df_cleaned

def save_cleaned_data(df, output_file_path):
    """Save the cleaned data to a new CSV file."""
    df.to_csv(output_file_path, index=False)
    print(f"Cleaned data saved to {output_file_path}")

if __name__ == "__main__":
    # Example: File paths
    input_file_path = 'data/raw/API_EN.ATM.CO2E.KT_DS2_en_csv_v2_32234.csv'  # Replace with your actual path
    output_file_path = 'data/cleaned/co2_emissions_cleaned.csv'  # Replace with your actual path
    
    # Load and clean data
    df = load_data(input_file_path)
    if df is not None:
        df_cleaned = clean_data(df)
        save_cleaned_data(df_cleaned, output_file_path)
