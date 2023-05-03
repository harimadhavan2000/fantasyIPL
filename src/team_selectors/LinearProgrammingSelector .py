import pandas as pd
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus

class LinearProgrammingSelector:
    def __init__(self, player_data, budget, max_players):
        self.player_data = player_data
        self.budget = budget
        self.max_players = max_players

    def select_team(self):
        # Initialize the linear programming problem
        prob = LpProblem("FantasyCricket", LpMaximize)

        # Create binary variables for each player
        player_vars = [LpVariable("x{}".format(i), cat="Binary") for i in range(len(self.player_data))]

        # Set the objective function: maximize the total predicted points of the team
        prob += lpSum([player_vars[i] * self.player_data.iloc[i]['Predicted Points'] for i in range(len(self.player_data))])

        # Constraints

        # Team budget constraint
        prob += lpSum([player_vars[i] * self.player_data.iloc[i]['Cost'] for i in range(len(self.player_data))]) <= self.budget

        # Number of players constraint
        prob += lpSum(player_vars) == self.max_players

        # Role-based constraints
        role_limits = {'Batsman': 5, 'Bowler': 5, 'All-rounder': 3, 'Wicketkeeper': 1}
        for role, limit in role_limits.items():
            prob += lpSum([player_vars[i] for i in range(len(self.player_data)) if self.player_data.iloc[i]['Player Role'] == role]) <= limit

        # Solve the linear programming problem
        prob.solve()

        # Create the best team
        selected_team = []
        for i in range(len(self.player_data)):
            if player_vars[i].varValue == 1:  # Player is included in the team
                player_name = self.player_data.iloc[i]['Player']
                player_role = self.player_data.iloc[i]['Player Role']
                player_cost = self.player_data.iloc[i]['Cost']
                selected_team.append((player_name, player_role, player_cost))

        return selected_team

# Instantiate the LinearProgrammingSelector class
lp_selector = LinearProgrammingSelector(ipl_extended_stats_df, budget=100, max_players=11)

# Select the best team using the Linear Programming approach
best_lp_team = lp_selector.select_team()

# Print the best team selected by the Linear Programming approach
print("Best team selected by Linear Programming:")
print(best_lp_team)
