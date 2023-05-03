# tests/test_data_preprocessing.py

import pandas as pd
from src.data_preprocessing import preprocess_data

def test_preprocess_data():
    # Create a sample DataFrame for testing
    sample_data = pd.DataFrame({"Player": ["A", "B"], "Cost": ["10", "20"], "Missing_Column": [0, 1]})

    # Preprocess the data using the preprocess_data function
    processed_data = preprocess_data(sample_data)

    # Check if the preprocess_data function correctly adds the missing column and converts the data types
    assert processed_data.shape == (2, 3)
    assert processed_data.dtypes["Player"] == "object"
    assert processed_data.dtypes["Cost"] == "float64"
    assert processed_data.dtypes["Missing_Column"] == "float64"
