
import pickle
import pandas as pd

def load_model(model_file_path):
    """ Load the trained model from a file. """
    try:
        with open(model_file_path, 'rb') as file:
            model = pickle.load(file)
        print(f"Model loaded successfully from {model_file_path}")
        return model
    except FileNotFoundError as e:
        print(f"Model file not found: {e}")
        return None

def make_prediction(model, input_data):
    """ Make predictions using the loaded model and input data. """
    predictions = model.predict(input_data)
    return predictions

if __name__ == "__main__":
    # Path to the saved model
    model_file_path = 'models/co2_model.pkl'  # Replace with the actual model file path

    # Load the model
    model = load_model(model_file_path)

    if model is not None:
        # Example input data (replace with actual data or dynamically load it)
        input_data = pd.DataFrame({
            'feature1': [6, 7, 8],  # Example feature columns
            'feature2': [7, 8, 9]
        })

        # Make predictions
        predictions = make_prediction(model, input_data)

        # Display the predictions
        print("Predictions for the input data:")
        print(predictions)
