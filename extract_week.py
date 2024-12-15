import os
import json
import pandas as pd

# Directory where the JSON files are stored
directory = '/Users/marcojonsson/FantasyDataScraping/espn_scraper/cached_data/apis/scoreboard'

# Path to the CSV containing player stats and game IDs
csv_file = '/Users/marcojonsson/FantasyDataScraping/espn_scraper/nfl_player_stats.csv'

# Load the CSV and extract the unique game IDs
df = pd.read_csv(csv_file)
csv_game_ids = set(df['GameID'].astype(str).str.strip())  # Ensure all game IDs are strings and stripped

# List to store game ID and week tuples
game_week_list = []

# Iterate through all JSON files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):  # Process only JSON files
        file_path = os.path.join(directory, filename)
        
        # Open and load the JSON file
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                events = data.get('events', [])
                for event in events:
                    uid = event.get('uid')  # Extract the full UID
                    if uid and 'e:' in uid:
                        game_id = uid.split('e:')[1].strip()  # Extract the part after 'e:' and strip whitespace
                        week_number = event.get('week', {}).get('number')  # Extract week number
                        
                        # Debugging output for comparison
                        # print(f"Extracted GameID: {game_id}, Week: {week_number}")
                        
                        if game_id in csv_game_ids:
                            # print(f"Match found for GameID: {game_id}")
                            game_week_list.append((game_id, week_number))
                        else:
                            print(f"No match for GameID: {game_id}")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in {filename}: {e}")


# Optionally, save this list to a CSV file
output_file = '/Users/marcojonsson/FantasyDataScraping/filtered_game_week_list.csv'
import csv

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['game_id', 'week'])  # Header
    writer.writerows(game_week_list)

print(f"Filtered game ID and week data saved to {output_file}.")
