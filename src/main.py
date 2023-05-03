from data_preprocessing import preprocess_data
from feature_extraction import calculate_feature1, calculate_feature2, calculate_feature3
from update_every_match import update_player_data
import pandas

def select_initial_team(player_data):
    selector = GreedySelector(player_data, budget=100, max_players=11)
    initial_team = selector.select_team()
    return initial_team

def run_season_simulation(player_data, initial_team):
    # Define a list of feature calculator functions
    feature_calculators = [calculate_feature1, calculate_feature2, calculate_feature3]

    # Loop through each match in the season
    for match_index in range(number_of_matches):
        # Load new match data (replace this with the actual loading of new match data)
        new_match_data = pd.read_csv(f"../data/new_match_data_{match_index}.csv")

        # Update player data and recompute features after each match
        updated_player_data = update_player_data(player_data, new_match_data, feature_calculators)

        # Instantiate the GreedySelectorLimitedChanges with the initial team and the maximum number of allowed changes
        selector = GreedySelectorLimitedChanges(updated_player_data, budget=100, max_players=11, initial_team=initial_team, max_changes=3)

        # Select a new team based on the updated player data and the limited number of allowed changes
        new_team = selector.select_team()

        # Update the initial team for the next match
        initial_team = new_team




# Load and preprocess the data
player_data = pd.read_csv("data/player_data.csv")
player_data = preprocess_data(player_data)

# Calculate features
feature_calculators = [calculate_feature1, calculate_feature2, calculate_feature3]
for feature_calculator in feature_calculators:
    player_data = feature_calculator(player_data)

# Select initial team and run the season simulation
initial_team = select_initial_team(player_data)
run_season_simulation(player_data, initial_team)

