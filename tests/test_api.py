import unittest
from unittest.mock import patch
import json
from app.api import app

class TestAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'API is running')

    @patch('app.api.model.predict')
    def test_prediction(self, mock_predict):
        mock_input = {
            "feature1": [6, 7, 8],
            "feature2": [7, 8, 9]
        }
        mock_predict.return_value = [1, 2, 3]  # Mocking the prediction

        response = self.app.post('/api/predict', data=json.dumps(mock_input), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('predictions', data)
        self.assertEqual(data['predictions'], [1, 2, 3])

if __name__ == '__main__':
    unittest.main()
