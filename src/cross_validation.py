from sklearn.model_selection import KFold
from team_selectors import GreedySelector, GeneticSelector, LinearProgrammingSelector
import pandas as pd

def cross_validate(model_class, player_data, n_splits=5):
    # Perform k-fold cross-validation and return the average performance across all folds
    kfold = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    total_performance = 0

    for train_index, test_index in kfold.split(player_data):
        train_data = player_data.iloc[train_index]
        test_data = player_data.iloc[test_index]

        # Instantiate the model and select the team
        model = model_class(train_data, budget=100, max_players=11)
        selected_team = model.select_team()

        # Calculate the total actual fantasy points of the selected team using test data
        selected_team_points = sum(test_data.loc[test_data['Player'] == player_name]['Actual Points'].values[0] for player_name, _, _ in selected_team)

        total_performance += selected_team_points

    return total_performance / n_splits

# Add a column for actual fantasy points in the historical data
ipl_historical_stats_df = pd.read_csv('../data/ipl_historical_stats.csv')
ipl_historical_stats_df['Actual Points'] = ...

# Cross-validate the performance of each algorithm
greedy_performance = cross_validate(GreedySelector, ipl_historical_stats_df)
genetic_performance = cross_validate(GeneticSelector, ipl_historical_stats_df)
lp_performance = cross_validate(LinearProgrammingSelector, ipl_historical_stats_df)

print("Average performance across all folds (k-fold cross-validation):")
print("Greedy Algorithm:", greedy_performance)
print("Genetic Algorithm:", genetic_performance)
print("Linear Programming:", lp_performance)
