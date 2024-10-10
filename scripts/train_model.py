import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
import pickle

def load_data_from_db(engine):
    """Load data from AWS RDS."""
    query = "SELECT * FROM emissions_data"
    df = pd.read_sql(query, engine)
    print("Data loaded successfully from the database.")
    return df

def preprocess_data(X, y):
    """Impute missing values in the feature matrix and target."""
    imputer = SimpleImputer(strategy='mean')  # You can also try 'median', 'most_frequent', etc.
    
    # Impute X (features)
    X_imputed = imputer.fit_transform(X)
    
    # Drop rows where y (target) is NaN
    non_nan_indices = y.notna()
    X_imputed = X_imputed[non_nan_indices]
    y = y[non_nan_indices]
    
    return X_imputed, y

def handle_missing_columns(df):
    """Drop columns with all missing values."""
    df = df.dropna(axis=1, how='all')
    return df

def train_model(X_train, y_train):
    """Train a model using GridSearchCV for hyperparameter tuning."""
    # Define models to test
    models = {
        'linear_regression': LinearRegression(),
        'random_forest': RandomForestRegressor(),
        'hist_gradient_boosting': HistGradientBoostingRegressor()  # Handles missing values natively
    }
    
    # Define parameters for tuning
    param_grid = {
        'linear_regression': {},
        'random_forest': {
            'n_estimators': [50, 100, 200],
            'max_depth': [10, 20, None]
        },
        'hist_gradient_boosting': {
            'max_iter': [100, 200],
            'max_depth': [10, 20, None]
        }
    }

    best_model = None
    best_score = float('inf')
    
    for model_name in models:
        print(f"Training {model_name}...")
        grid = GridSearchCV(models[model_name], param_grid[model_name], cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
        grid.fit(X_train, y_train)
        
        print(f"Best parameters for {model_name}: {grid.best_params_}")
        print(f"Best score for {model_name}: {-grid.best_score_}")
        
        if -grid.best_score_ < best_score:
            best_score = -grid.best_score_
            best_model = grid.best_estimator_

    print("Best model selected.")
    return best_model

def evaluate_model(model, X_test, y_test):
    """Evaluate the model's performance."""
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")
    print(f"R^2 Score: {r2}")
    return mse, r2

def save_model(model, output_file_path):
    """Save the trained model to a file using pickle."""
    with open(output_file_path, 'wb') as file:
        pickle.dump(model, file)
    print(f"Model saved to {output_file_path}")

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from dotenv import load_dotenv
    import os

    # Load environment variables
    load_dotenv()

    # Database connection
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)

    # Load the cleaned data from the database
    df = load_data_from_db(engine)

    if df is not None:
        # Drop columns with all missing values
        df = handle_missing_columns(df)

        # Define features (X) and target (y)
        X = df.iloc[:, 5:]  # Assuming numerical features start from the 5th column onward
        y = df['2020']  # Adjust target column to the year of interest (e.g., '2020')

        # Preprocess the data to handle NaNs in both X and y
        X_imputed, y_cleaned = preprocess_data(X, y)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X_imputed, y_cleaned, test_size=0.2, random_state=42)

        # Train the model with hyperparameter tuning
        model = train_model(X_train, y_train)

        # Evaluate the model
        evaluate_model(model, X_test, y_test)

        # Save the best model
        model_output_path = 'models/co2_best_model.pkl'
        save_model(model, model_output_path)
