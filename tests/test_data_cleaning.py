import unittest
import pandas as pd
from scripts.data_cleaning import clean_data

class TestDataCleaning(unittest.TestCase):
    
    def setUp(self):
        # Example raw data for testing
        data = {
            'Country Name': ['Country A', 'Country B', 'Country C'],
            'Year 1': [10, 20, None],
            'Year 2': [15, None, 30],
            'Year 3': [None, 25, 35]
        }
        self.df = pd.DataFrame(data)
    
    def test_clean_data(self):
        # Run the data cleaning function
        df_cleaned = clean_data(self.df)
        
        # Check if missing values are filled
        self.assertFalse(df_cleaned.isnull().values.any(), "There are still missing values in the cleaned data")
        
        # Check if the shape of the DataFrame remains unchanged
        self.assertEqual(df_cleaned.shape, self.df.shape, "DataFrame shape changed after cleaning")
    
    def tearDown(self):
        # Clean up (if necessary)
        pass

if __name__ == '__main__':
    unittest.main()
