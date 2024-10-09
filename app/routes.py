
from flask import Flask, render_template, jsonify, request
import pandas as pd
import pickle

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for visualizations or data summary
@app.route('/summary')
def summary():
    # Example: Load a summary of the CO2 data
    data_path = 'path_to_cleaned_data.csv'  # Replace with actual path
    df = pd.read_csv(data_path)
    summary_data = df.describe().to_dict()
    return jsonify(summary_data)

# Route to predict CO2 emissions (if using a model)
@app.route('/predict', methods=['POST'])
def predict():
    model_path = 'models/co2_model.pkl'  # Path to your trained model
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        # Get the data from the POST request
        data = request.get_json()
        input_data = pd.DataFrame(data)
        prediction = model.predict(input_data)
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
