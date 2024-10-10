import os
from flask import Flask, request, jsonify, abort
import pandas as pd
import pickle
import logging
from sklearn.exceptions import NotFittedError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Load the trained model
model_path = 'models/co2_model.pkl'

def load_model(model_path):
    """ Load the trained model from a file. """
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        logging.info(f"Model loaded successfully from {model_path}")
        return model
    except FileNotFoundError:
        logging.error(f"Model file not found: {model_path}")
        return None
    except Exception as e:
        logging.error(f"Error loading the model: {e}")
        return None

# Load the model
model = load_model(model_path)

# API endpoint to make predictions
@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            abort(500, description='Model is not available')
        
        input_data = request.get_json()

        if not input_data:
            abort(400, description='No input data provided')

        # Assuming your model expects a DataFrame with certain columns
        input_df = pd.DataFrame(input_data)
        if input_df.isnull().values.any():
            abort(400, description='Input data contains missing values')
        
        # Validate input format
        expected_columns = ['feature1', 'feature2']  # Replace with actual expected feature names
        if not all(col in input_df.columns for col in expected_columns):
            abort(400, description=f"Expected columns: {expected_columns}")

        try:
            predictions = model.predict(input_df)
        except NotFittedError:
            abort(500, description="Model is not fitted correctly.")
        
        return jsonify({'predictions': predictions.tolist()})
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

# API endpoint for health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'API is running'}), 200

if __name__ == '__main__':
    app.run(debug=True)
