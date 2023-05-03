# Import additional libraries
from sklearn.metrics import mean_squared_error

# Load the extended IPL player stats with additional features
ipl_extended_stats_df = pd.read_csv("../data/ipl_player_stats_with_extended_features.csv")

# Add the new features to the existing list of features
extended_features = features + [
    "Player Form",
    "Opposition Strength",
    "Home Performance",
    "Away Performance",
    "Pitch Condition Performance",
    "Weather Condition Performance",
    "Player Role",
    "Batting Position",
]

# Prepare the data for training and testing with the extended features
X_extended = ipl_extended_stats_df[extended_features]

# Split the dataset into training and testing sets with the extended features
X_train_extended, X_test_extended, y_train_extended, y_test_extended = train_test_split(
    X_extended, y, test_size=0.2, random_state=42
)

# Normalize the extended features using Min-Max Scaling
X_train_extended_scaled = scaler.fit_transform(X_train_extended)
X_test_extended_scaled = scaler.transform(X_test_extended)

# Train a Random Forest Regressor model with the extended features
rf_regressor_extended = RandomForestRegressor(n_estimators=100, random_state=42)
rf_regressor_extended.fit(X_train_extended_scaled, y_train_extended)

# Evaluate the model performance on the test set with the extended features
y_pred_extended = rf_regressor_extended.predict(X_test_extended_scaled)
rmse_extended = np.sqrt(mean_squared_error(y_test_extended, y_pred_extended))

# Compare the model performance before and after adding the new features
y_pred = rf_regressor.predict(X_test_scaled)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"RMSE before adding new features: {rmse}")
print(f"RMSE after adding new features: {rmse_extended}")

if rmse_extended < rmse:
    print("The extended model has improved performance.")
else:
    print("The extended model did not show significant improvement.")
