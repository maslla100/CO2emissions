import pickle
import pandas as pd

def load_model(model_file_path):
    try:
        with open(model_file_path, 'rb') as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError as e:
        print(f"Model file not found: {e}")
        return None

def make_prediction(model, input_data):
    predictions = model.predict(input_data)
    return predictions

if __name__ == "__main__":
    model_file_path = 'models/co2_model.pkl'
    model = load_model(model_file_path)

    if model is not None:
        input_data = pd.DataFrame({
            'feature1': [6, 7, 8],
            'feature2': [7, 8, 9]
        })

        predictions = make_prediction(model, input_data)
        print(f"Predictions: {predictions}")
