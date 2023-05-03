# tests/test_feature_extraction.py

import pandas as pd
from src.feature_extraction import calculate_feature1

def test_calculate_feature1():
    # Create a sample DataFrame for testing
    sample_data = pd.DataFrame({"Player": ["A", "B"], "Fantasy_Points": [10, 20], "Matches_Played": [1, 2]})

    # Calculate the feature using the calculate_feature1 function
    calculated_data = calculate_feature1(sample_data)

    # Check if the calculate_feature1 function correctly calculates the feature
    assert calculated_data.shape == (2, 4)
    assert calculated_data["Feature1"].equals(pd.Series([10, 10], name="Feature1"))
