
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pickle

def load_data(file_path):
    """ Load the cleaned dataset for model training. """
    try:
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully from {file_path}")
        return df
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return None

def train_model(X_train, y_train):
    """ Train a Linear Regression model. """
    model = LinearRegression()
    model.fit(X_train, y_train)
    print("Model training completed.")
    return model

def evaluate_model(model, X_test, y_test):
    """ Evaluate the model's performance. """
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")
    print(f"R^2 Score: {r2}")
    return mse, r2

def save_model(model, output_file_path):
    """ Save the trained model to a file using pickle. """
    with open(output_file_path, 'wb') as file:
        pickle.dump(model, file)
    print(f"Model saved to {output_file_path}")

if __name__ == "__main__":
    # File paths
    input_file_path = 'data/cleaned/co2_emissions_cleaned.csv'  # Replace with your actual path
    model_output_path = 'models/co2_model.pkl'  # Path to save the trained model
    
    # Load the cleaned data
    df = load_data(input_file_path)
    
    if df is not None:
        # Define features (X) and target (y)
        X = df.iloc[:, 2:]  # Example: features are columns from index 2 onwards
        y = df.iloc[:, 1]   # Example: target is the second column (CO2 emissions)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = train_model(X_train, y_train)

        # Evaluate the model
        evaluate_model(model, X_test, y_test)

        # Save the trained model
        save_model(model, model_output_path)
