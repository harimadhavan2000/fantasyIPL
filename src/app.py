import streamlit as st
import pandas as pd
# Import your custom selector classes
from team_selectors import GreedySelector, GeneticSelector, LinearProgrammingSelector

# Load the preprocessed player data (assuming you have saved it as 'preprocessed_player_data.csv')
player_data = pd.read_csv('../data/preprocessed_player_data.csv')

# Define a mapping between algorithm names and classes
algorithm_mapping = {
    'Greedy Algorithm': GreedySelector,
    'Genetic Algorithm': GeneticSelector,
    'Linear Programming': LinearProgrammingSelector
}

st.title("Fantasy Cricket Team Selector")

# User inputs
budget = st.number_input("Enter your budget:", min_value=0, value=100, step=1)
algorithm = st.selectbox("Select an algorithm:", options=list(algorithm_mapping.keys()))

# Button to generate the team
if st.button("Generate Team"):
    # Instantiate the selected algorithm
    selector_class = algorithm_mapping[algorithm]
    selector = selector_class(player_data, budget=budget, max_players=11)

    # Generate the team
    selected_team = selector.select_team()

    # Display the team
    st.header("Selected Team")
    team_df = pd.DataFrame(selected_team, columns=["Player Name", "Player Role", "Cost"])
    st.write(team_df)

    # Display additional statistics or information, if needed
    # ...
