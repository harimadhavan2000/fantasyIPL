# tests/test_team_selectors.py

import pandas as pd
from src.team_selectors import GreedySelector, LinearProgrammingSelector, GreedySelectorLimitedChanges, LinearProgrammingSelectorLimitedChanges

def test_greedy_selector():
    sample_data = pd.DataFrame({"Player": ["A", "B", "C"], "Cost": [10, 20, 30], "Fantasy_Points": [30, 20, 10]})
    selector = GreedySelector(sample_data, budget=50, max_players=2)
    team = selector.select_team()

    assert len(team) == 2
    assert team["Player"].isin(["A", "B"]).all()
    assert team["Cost"].sum() <= 50

def test_linear_programming_selector():
    sample_data = pd.DataFrame({"Player": ["A", "B", "C"], "Cost": [10, 20, 30], "Fantasy_Points": [30, 20, 10]})
    selector = LinearProgrammingSelector(sample_data, budget=50, max_players=2)
    team = selector.select_team()

    assert len(team) == 2
    assert team["Player"].isin(["A", "B"]).all()
    assert team["Cost"].sum() <= 50

def test_greedy_selector_limited_changes():
    sample_data = pd.DataFrame({"Player": ["A", "B", "C"], "Cost": [10, 20, 30], "Fantasy_Points": [30, 20, 10]})
    initial_team = pd.DataFrame({"Player": ["A", "C"], "Cost": [10, 30], "Fantasy_Points": [30, 10]})
    selector = GreedySelectorLimitedChanges(sample_data, budget=50, max_players=2, initial_team=initial_team, max_changes=1)
    new_team = selector.select_team()

    assert len(new_team) == 2
    assert new_team["Player"].isin(["A", "B"]).all()
    assert new_team["Cost"].sum() <= 50

def test_linear_programming_selector_limited_changes():
    sample_data = pd.DataFrame({"Player": ["A", "B", "C"], "Cost": [10, 20, 30], "Fantasy_Points": [30, 20, 10]})
    initial_team = pd.DataFrame({"Player": ["A", "C"], "Cost": [10, 30], "Fantasy_Points": [30, 10]})
    selector = LinearProgrammingSelectorLimitedChanges(sample_data, budget=50, max_players=2, initial_team=initial_team, max_changes=1)
    new_team = selector.select_team()

    assert len(new_team) == 2
    assert new_team["Player"].isin(["A", "B"]).all()
    assert new_team["Cost"].sum() <= 50
