
from flask import Flask, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

# Load the trained model
model_path = 'models/co2_model.pkl'  # Path to your trained model

def load_model(model_path):
    """ Load the trained model from a file. """
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        print(f"Model loaded successfully from {model_path}")
        return model
    except Exception as e:
        print(f"Error loading the model: {e}")
        return None

model = load_model(model_path)

# API endpoint to make predictions
@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        # Get input data from the request
        input_data = request.get_json()
        input_df = pd.DataFrame(input_data)
        
        # Make predictions using the loaded model
        predictions = model.predict(input_df)
        return jsonify({'predictions': predictions.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint for health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'API is running'}), 200

if __name__ == '__main__':
    app.run(debug=True)
