import pandas as pd

# Load the IPL player stats from the CSV file created in the first step
ipl_stats_df = pd.read_csv("../data/ipl_player_stats.csv")

# Calculate the Batting Average
ipl_stats_df["Batting Average"] = ipl_stats_df["Runs"]/ipl_stats_df["Dismissals"]

# Calculate the Strike Rate
ipl_stats_df["Strike Rate"] = (ipl_stats_df["Runs"]/ipl_stats_df["Balls"])*100

# Calculate the Bowling Average
ipl_stats_df["Bowling Average"] = ipl_stats_df["Runs conceded"]/ipl_stats_df["Wkts"]

# Calculate the Economy Rate
ipl_stats_df["Economy Rate"] = ipl_stats_df["Runs conceded"]/ipl_stats_df["Overs"]

# Replace any NaN values with 0
ipl_stats_df.fillna(0, inplace=True)

# Save the DataFrame with the new features to a CSV file
ipl_stats_df.to_csv("../data/ipl_player_stats_with_features.csv", index=False)
