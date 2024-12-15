import pandas as pd

# Paths to the files
player_stats_file = '/Users/marcojonsson/FantasyDataScraping/espn_scraper/nfl_player_stats.csv'
filtered_game_week_file = '/Users/marcojonsson/FantasyDataScraping/filtered_game_week_list.csv'
output_file = '/Users/marcojonsson/FantasyDataScraping/espn_scraper/nfl_player_stats_with_week.csv'

# Load the player stats CSV
player_stats_df = pd.read_csv(player_stats_file)

# Load the filtered game-week list CSV
game_week_df = pd.read_csv(filtered_game_week_file)

# Check columns in both DataFrames before merging
# print("Player Stats Columns:", player_stats_df.columns)
# print("Game Week Columns:", game_week_df.columns)

# Ensure column names match (rename if necessary)
game_week_df.rename(columns={'game_id': 'GameID', 'week': 'Week'}, inplace=True)

# Merge the player stats with the game-week data
merged_df = player_stats_df.merge(game_week_df, on='GameID', how='left')

# Drop the 'interceptions.1' column if it exists in the merged DataFrame
if 'interceptions.1' in merged_df.columns:
    merged_df.drop(columns=['interceptions.1'], inplace=True)

# Save the updated DataFrame to a new CSV file
merged_df.to_csv(output_file, index=False)

print(f"Updated CSV with week column saved to {output_file}.")
