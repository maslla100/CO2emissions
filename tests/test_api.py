
import unittest
import json
from flask import Flask
from app.api import app  # Assuming 'api.py' is in the 'app' folder

class TestAPI(unittest.TestCase):
    
    def setUp(self):
        # Set up the test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        # Test the health check endpoint
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'API is running')

    def test_prediction(self):
        # Test the prediction endpoint with mock input data
        mock_input = {
            "feature1": [6, 7, 8],
            "feature2": [7, 8, 9]
        }
        response = self.app.post('/api/predict', data=json.dumps(mock_input), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('predictions', data)
        self.assertIsInstance(data['predictions'], list)

if __name__ == '__main__':
    unittest.main()
