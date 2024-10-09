
import unittest
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle

class TestModelTraining(unittest.TestCase):
    
    def setUp(self):
        # Example training data
        X = np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]])
        y = np.array([2, 3, 4, 5, 6])
        
        # Split the data into training and test sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train a simple Linear Regression model
        self.model = LinearRegression()
        self.model.fit(self.X_train, self.y_train)
        
        # Save the model using pickle (mocking real use case)
        self.model_file = 'test_model.pkl'
        with open(self.model_file, 'wb') as file:
            pickle.dump(self.model, file)
    
    def test_model_training(self):
        # Check if the model was trained successfully
        y_pred_train = self.model.predict(self.X_train)
        self.assertEqual(len(y_pred_train), len(self.y_train), "Model training failed")
    
    def test_model_prediction(self):
        # Test model prediction accuracy on the test set
        y_pred_test = self.model.predict(self.X_test)
        mse = mean_squared_error(self.y_test, y_pred_test)
        self.assertLess(mse, 0.1, "Model test predictions are not accurate enough")
    
    def tearDown(self):
        # Clean up the saved model file
        import os
        if os.path.exists(self.model_file):
            os.remove(self.model_file)

if __name__ == '__main__':
    unittest.main()
