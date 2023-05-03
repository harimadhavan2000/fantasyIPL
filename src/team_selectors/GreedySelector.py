import pandas as pd

class GreedySelector:
    def __init__(self, player_data, budget, max_players):
        self.player_data = player_data
        self.budget = budget
        self.max_players = max_players

    def select_team(self):
        # Sort the players by predicted fantasy points in descending order
        sorted_players = self.player_data.sort_values(by='Predicted Points', ascending=False)

        # Initialize the team and budget
        selected_team = []
        remaining_budget = self.budget

        # Iterate through the sorted players
        for _, player in sorted_players.iterrows():
            player_name = player['Player']
            player_cost = player['Cost']
            player_role = player['Player Role']

            # Check if adding the player to the team is possible within the budget and player constraints
            if remaining_budget >= player_cost and self._valid_position(selected_team, player_role):
                # Add the player to the team and update the budget
                selected_team.append((player_name, player_role, player_cost))
                remaining_budget -= player_cost

            # Stop the loop if the team is full
            if len(selected_team) == self.max_players:
                break

        return selected_team

    def _valid_position(self, team, player_role):
        # Check if adding a player with the given role to the team would violate the constraints

        # Count the number of players with the same role in the team
        role_count = sum(1 for _, role, _ in team if role == player_role)

        # Define the maximum number of players allowed for each role
        role_limits = {
            'Batsman': 5,
            'Bowler': 5,
            'All-rounder': 3,
            'Wicketkeeper': 1,
        }

        return role_count < role_limits[player_role]

# Instantiate the GreedySelector class
greedy_selector = GreedySelector(ipl_extended_stats_df, budget=100, max_players=11)

# Select the best team using the Greedy Algorithm
best_greedy_team = greedy_selector.select_team()

# Print the best team selected by the Greedy Algorithm
print("Best team selected by Greedy Algorithm:")
print(best_greedy_team)
