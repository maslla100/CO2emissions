from flask import Flask, request, jsonify, abort
import pandas as pd
import pickle
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Load the trained model
model_path = 'models/co2_model.pkl'  # Path to your trained model

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
        
        input_df = pd.DataFrame(input_data)

        if input_df.isnull().values.any():
            abort(400, description='Input data contains missing values')
        
        predictions = model.predict(input_df)

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
