import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set the base URL for the ESPN Cricinfo IPL statistics page
base_url = "https://stats.espncricinfo.com/ci/engine/records/averages/batting_bowling_by_team.html?id=117;team=4348;type=trophy"

# Send an HTTP request to the URL and parse the HTML content
response = requests.get(base_url)
soup = BeautifulSoup(response.content, "html.parser")

# Find the table containing the player statistics
stats_table = soup.find("table", class_="engineTable")

# Extract the header row and data rows from the table
header_row = stats_table.find("thead").find("tr")
data_rows = stats_table.find("tbody").find_all("tr")

# Extract column names from the header row
column_names = [th.text for th in header_row.find_all("th")]

# Extract player statistics from the data rows
player_stats = []
for row in data_rows:
    stats = [td.text for td in row.find_all("td")]
    player_stats.append(stats)

# Create a pandas DataFrame with the collected data
ipl_stats_df = pd.DataFrame(player_stats, columns=column_names)

# Clean the DataFrame (remove unnecessary characters and convert data types)
ipl_stats_df.replace("-", "", inplace=True)
ipl_stats_df.replace("", pd.NA, inplace=True)
ipl_stats_df.dropna(how="all", inplace=True)

# Save the DataFrame to a CSV file
ipl_stats_df.to_csv("../data/ipl_player_stats.csv", index=False)
