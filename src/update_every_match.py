import pandas as pd

def update_player_data(player_data, new_match_data, feature_calculators):
    """
    Update player data and recompute features after each match.
    
    Args:
    player_data (pd.DataFrame): The player data containing historical performance.
    new_match_data (pd.DataFrame): The data for the new match.
    feature_calculators (List[Callable]): A list of functions to calculate the features.
    
    Returns:
    pd.DataFrame: Updated player data with recalculated features.
    """
    # Update player data with the new match data
    updated_player_data = pd.concat([player_data, new_match_data], ignore_index=True)

    # Recalculate features using the feature_calculators
    for feature_calculator in feature_calculators:
        updated_player_data = feature_calculator(updated_player_data)

    return updated_player_data


# Load new match data (replace this with the actual loading of new match data)
new_match_data = pd.read_csv("../data/new_match_data.csv")

# Define a list of feature calculator functions (replace this with your actual feature calculators)
feature_calculators = [calculate_feature1, calculate_feature2, calculate_feature3]

# Update player data and recompute features after each match
updated_player_data = update_player_data(player_data, new_match_data, feature_calculators)