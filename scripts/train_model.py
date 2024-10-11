import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import pickle

def load_data_from_db(engine):
    """Load data from AWS RDS."""
    query = "SELECT * FROM emissions_data"
    df = pd.read_sql(query, engine)
    print("Data loaded successfully from the database.")
    return df

def preprocess_data(X, y):
    """Impute missing values in the feature matrix and target."""
    imputer = SimpleImputer(strategy='mean')
    X_imputed = imputer.fit_transform(X)
    non_nan_indices = y.notna()
    X_imputed = X_imputed[non_nan_indices]
    y = y[non_nan_indices]
    return X_imputed, y

def handle_missing_columns(df):
    """Drop columns with all missing values."""
    df = df.dropna(axis=1, how='all')
    return df

def train_model(X_train, y_train):
    models = {
        'linear_regression': LinearRegression(),
        'random_forest': RandomForestRegressor(),
        'hist_gradient_boosting': HistGradientBoostingRegressor()
    }
    
    param_grid = {
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
    
    for model_name, model in models.items():
        print(f"Training {model_name}...")
        grid = GridSearchCV(model, param_grid.get(model_name, {}), cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
        grid.fit(X_train, y_train)
        
        print(f"Best score for {model_name}: {-grid.best_score_}")
        if -grid.best_score_ < best_score:
            best_score = -grid.best_score_
            best_model = grid.best_estimator_

    return best_model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"MSE: {mse}, R²: {r2}")
    plt.figure(figsize=(10,6))
    plt.plot(y_test.values, label='Actual CO2 Emissions')
    plt.plot(y_pred, label='Predicted CO2 Emissions', linestyle='dashed')
    plt.legend()
    plt.title('Actual vs Predicted CO2 Emissions')
    plt.xlabel('Index (Test Data)')
    plt.ylabel('CO2 Emissions (kt)')
    plt.show()
    
    return mse, r2

def save_model(model, output_file_path):
    with open(output_file_path, 'wb') as file:
        pickle.dump(model, file)
    print(f"Model saved to {output_file_path}")

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from dotenv import load_dotenv
    import os

    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)

    df = load_data_from_db(engine)
    if df is not None:
        df = handle_missing_columns(df)
        X = df.iloc[:, 5:]  
        y = df['2020']

        X_imputed, y_cleaned = preprocess_data(X, y)
        X_train, X_test, y_train, y_test = train_test_split(X_imputed, y_cleaned, test_size=0.2, random_state=42)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
        save_model(model, 'models/co2_best_model.pkl')
