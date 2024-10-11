import os
from flask import Blueprint, request, jsonify, abort
import pandas as pd
import pickle
import logging
from sklearn.exceptions import NotFittedError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create a blueprint for API endpoints
api_bp = Blueprint('api_bp', __name__)

# Construct the absolute path to the model file
current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory where api.py is located
model_path = os.path.join('models', 'co2_best_model.pkl')  # Construct the full path to the model file

def load_model(model_path):
    """Load the trained model from a file."""
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
@api_bp.route('/api/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            logging.error("Model is not available")
            abort(500, description='Model is not available')

        input_data = request.get_json()
        logging.info(f"Received input data: {input_data}")

        if not input_data:
            logging.error("No input data provided for prediction")
            abort(400, description='No input data provided')

        # Convert input to DataFrame
        input_df = pd.DataFrame(input_data, index=[0])

        # Check for missing values in input
        if input_df.isnull().values.any():
            logging.error("Input data contains missing values")
            abort(400, description='Input data contains missing values')

        # List of features expected by the model (Replace with actual feature names)
        expected_columns = ['feature1', 'feature2', 'feature3', 'feature4', 'feature5', 'feature6', 
                            'feature7', 'feature8', 'feature9', 'feature10', 'feature11', 'feature12', 
                            'feature13', 'feature14', 'feature15', 'feature16', 'feature17', 'feature18', 
                            'feature19', 'feature20', 'feature21', 'feature22', 'feature23', 'feature24', 
                            'feature25', 'feature26', 'feature27', 'feature28', 'feature29', 'feature30', 
                            'feature31']  # Replace with the actual features your model expects.

        # Add missing columns with default value 0 if not provided
        for col in expected_columns:
            if col not in input_df.columns:
                input_df[col] = 0

        # Ensure the DataFrame has the correct number of features
        input_df = input_df[expected_columns]
        logging.info(f"Final input data for prediction: {input_df}")

        # Make predictions
        try:
            predictions = model.predict(input_df)
            logging.info("Prediction successful")
            return jsonify({'predictions': predictions.tolist()})
        
        except NotFittedError:
            logging.error("Model is not fitted correctly")
            abort(500, description="Model is not fitted correctly.")
    
    except Exception as e:
        logging.error(f"An error occurred during prediction: {str(e)}")
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

