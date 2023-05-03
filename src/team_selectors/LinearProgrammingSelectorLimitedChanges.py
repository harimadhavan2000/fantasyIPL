from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, LpInteger

class LinearProgrammingSelectorLimitedChanges:
    def __init__(self, player_data, budget, max_players, initial_team, max_changes):
        self.player_data = player_data
        self.budget = budget
        self.max_players = max_players
        self.initial_team = set(initial_team)
        self.max_changes = max_changes

    def select_team(self):
        # Create the Linear Programming problem
        prob = LpProblem("Fantasy_Cricket_Team_Selection", LpMaximize)

        # Define the decision variables
        player_vars = [LpVariable(f"player_{i}", cat=LpInteger, lowBound=0, upBound=1) for i in range(len(self.player_data))]

        # Objective function
        prob += lpSum(player_vars[i] * self.player_data.loc[i, 'Predicted Points'] for i in range(len(self.player_data)))

        # Constraints
        prob += lpSum(player_vars[i] * self.player_data.loc[i, 'Cost'] for i in range(len(self.player_data))) <= self.budget
        prob += lpSum(player_vars) == self.max_players

        # Limited number of player changes constraint
        prob += lpSum(player_vars[i] * (1 if i in self.initial_team else 0) for i in range(len(self.player_data))) >= (self.max_players - self.max_changes)

        # Solve the problem
        prob.solve()

        # Extract the selected team
        selected_team = [(self.player_data.loc[i, 'Player'], self.player_data.loc[i, 'Role'], self.player_data.loc[i, 'Cost']) for i in range(len(self.player_data)) if player_vars[i].value() == 1]

        return selected_team