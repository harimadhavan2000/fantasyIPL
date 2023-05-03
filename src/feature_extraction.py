import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# Load the IPL player stats with features from the CSV file created in the second step
ipl_stats_df = pd.read_csv("../data/ipl_player_stats_with_features.csv")

# Define a function to calculate fantasy points based on IPL scoring rules
def calculate_fantasy_points(row):
    batting_points = row['Runs'] + 2 * row['Fours'] + 6 * row['Sixes']
    bowling_points = 20 * row['Wkts'] + 10 * row['Mdns']
    fielding_points = 10 * (row['Catches'] + row['Stumpings'] + row['Run Outs'])

    return batting_points + bowling_points + fielding_points

# Calculate fantasy points for each player
ipl_stats_df['Fantasy Points'] = ipl_stats_df.apply(calculate_fantasy_points, axis=1)

# Select features and target variable
features = ['Batting Average', 'Strike Rate', 'Bowling Average', 'Economy Rate']
target = 'Fantasy Points'

# Prepare the data for training and testing
X = ipl_stats_df[features]
y = ipl_stats_df[target]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize the features using Min-Max Scaling
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train a Random Forest Regressor model to find feature importance
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
rf_regressor.fit(X_train_scaled, y_train)

# Calculate the feature importance and sort them in descending order
feature_importance = pd.DataFrame({
    'Feature': features,
    'Importance': rf_regressor.feature_importances_
}).sort_values(by='Importance', ascending=False)

# Assign weights to features based on their importance
weights = feature_importance.set_index('Feature')['Importance'].to_dict()

# Calculate the weighted score for each player
ipl_stats_df['Weighted Score'] = (
    ipl_stats_df['Batting Average'] * weights['Batting Average'] +
    ipl_stats_df['Strike Rate'] * weights['Strike Rate'] +
    ipl_stats_df['Bowling Average'] * weights['Bowling Average'] +
    ipl_stats_df['Economy Rate'] * weights['Economy Rate']
)

# Save the DataFrame with the weighted scores to a CSV file
ipl_stats_df.to_csv("../data/ipl_player_stats_with_weighted_scores.csv", index=False)
