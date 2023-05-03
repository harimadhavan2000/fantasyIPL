class GreedySelectorLimitedChanges:
    def __init__(self, player_data, budget, max_players, initial_team, max_changes):
        self.player_data = player_data
        self.budget = budget
        self.max_players = max_players
        self.initial_team = set(initial_team)
        self.max_changes = max_changes

    def select_team(self):
        # Sort the player data by the ratio of predicted points to cost
        sorted_player_data = self.player_data.sort_values(by="Points/Cost", ascending=False)

        # Initialize the selected team and remaining budget
        selected_team = list(self.initial_team)
        remaining_budget = self.budget - sum(self.player_data.loc[player, "Cost"] for player in selected_team)
        
        # Greedy selection of players
        for i, row in sorted_player_data.iterrows():
            if len(selected_team) < self.max_players and i not in selected_team and row["Cost"] <= remaining_budget:
                # Check if the change doesn't exceed the allowed number of changes
                if (len(selected_team) - len(self.initial_team.intersection(selected_team))) < self.max_changes:
                    selected_team.append(i)
                    remaining_budget -= row["Cost"]

        # Return the selected team
        return [(self.player_data.loc[player, "Player"], self.player_data.loc[player, "Role"], self.player_data.loc[player, "Cost"]) for player in selected_team]