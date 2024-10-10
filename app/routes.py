import os
from flask import Flask, render_template, jsonify, request, abort
import pandas as pd
import pickle
import logging
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# Load database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("No DATABASE_URL set for PostgreSQL connection")

# Connect to PostgreSQL using SQLAlchemy
engine = create_engine(DATABASE_URL)

# Load the trained model once
model_path = 'models/co2_model.pkl'

def load_model(model_path):
    """ Load the trained model from a file. """
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        logging.info(f"Model loaded successfully from {model_path}")
        return model
    except Exception as e:
        logging.error(f"Error loading the model: {e}")
        return None

model = load_model(model_path)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for visualizations or data summary
@app.route('/summary')
def summary():
    try:
        df = pd.read_sql("SELECT * FROM emissions_data", engine)

        if df.empty:
            abort(404, description="Dataset is empty")
        
        summary_data = df.describe().to_dict()
        return jsonify(summary_data)
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

# Route to predict CO2 emissions
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        abort(500, description="Model not available")

    try:
        input_data = request.get_json()

        if not input_data:
            abort(400, description="No input data provided")

        input_df = pd.DataFrame(input_data)

        if input_df.isnull().values.any():
            abort(400, description="Input data contains missing values")
        
        predictions = model.predict(input_df)
        return jsonify({'predictions': predictions.tolist()})
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
