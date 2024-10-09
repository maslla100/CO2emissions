
import pandas as pd

def load_data(file_path):
    """ Load the CO2 emissions dataset. """
    try:
        df = pd.read_csv(file_path, skiprows=4)  # Adjust for file structure (skip metadata rows)
        print(f"Data loaded successfully from {file_path}")
        return df
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return None

def clean_data(df):
    """ Clean and preprocess the CO2 emissions data. """
    # Remove unnamed columns
    df_cleaned = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # Fill missing values with forward fill method
    df_cleaned.fillna(method='ffill', inplace=True)
    
    # Drop rows with all NaN values (in case of incomplete rows)
    df_cleaned.dropna(how='all', inplace=True)
    
    print("Data cleaning completed.")
    return df_cleaned

def save_cleaned_data(df, output_file_path):
    """ Save the cleaned data to a new CSV file. """
    df.to_csv(output_file_path, index=False)
    print(f"Cleaned data saved to {output_file_path}")

if __name__ == "__main__":
    # File paths
    input_file_path = 'path_to_raw_data.csv'  # Replace with your actual path
    output_file_path = 'path_to_cleaned_data.csv'  # Replace with your actual path
    
    # Load raw data
    df = load_data(input_file_path)
    
    # Clean and preprocess the data
    if df is not None:
        df_cleaned = clean_data(df)
        
        # Save the cleaned data
        save_cleaned_data(df_cleaned, output_file_path)
