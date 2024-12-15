## MUST RUN FROM FantasyDatascraping/espn_scraper (in same level as fantasy_csv_generator)

import json
import csv
import os

def load_json(season_type, week):
    # Dynamically construct the file path based on season type and week
    file_path = f"/Users/marcojonsson/FantasyDataScraping/espn_scraper/cached_data/apis/scoreboard/https:||site.api.espn.com|apis|site|v2|sports|football|nfl|scoreboard?dates=2023&seasontype={season_type}&week={week}.json"


    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        print(f"File for season type {season_type}, week {week} not found.")
        return None

def generate_csv():
    output_data=[]
    # Define the CSV headers
    headers = ['Week', 'Game ID', 'Team', 'Player Name', 'Position', 'Passing Yards', 'Rushing Yards', 'Receiving Yards', 'Touchdowns']
    
    # Prepare a list to store the data rows
    csv_data = []

    # Loop through season types and weeks you want to process
    # Define the week ranges for each season type
    season_week_ranges = {
        1: range(1, 5),    # Type 1: Weeks 1-4
        2: range(1, 19),   # Type 2: Weeks 1-18
        3: range(1, 6),    # Type 3: Weeks 1-5
        4: range(1, 2),    # Type 4: Week 1 only
    }

    # Loop through each season type and its corresponding week range
    # for season_type, weeks in season_week_ranges.items():
    #     for week in weeks:
    #         data = load_json(season_type, week)
    #         if data:

    #             for event in data['events']:
                    
    #                 #HEY THIS WORKS
    #                 for competition in event['competitions']:
    #                     # Loop through leaders for each competition
    #                     for leader in competition.get('leaders', []):
    #                         stat_name = leader.get('name', 'Unknown Stat')
    #                         stat_display_name = leader.get('displayName', 'Unknown Stat Type')
    #                         print(f"Stat: {stat_display_name} ({stat_name})")

    #                         # Loop through the leaders (players) for each stat
    #                         for player in leader.get('leaders', []):
    #                             player_name = player.get('athlete', {}).get('displayName', 'Unknown Player')
    #                             player_team = player.get('athlete', {}).get('team', {}).get('id', 'Unknown Team')
    #                             player_position = player.get('athlete', {}).get('position', {}).get('abbreviation', 'Unknown Position')
    #                             player_value = player.get('displayValue', 'No Value')

    #                             print(f"Player: {player_name} | Position: {player_position} | Team ID: {player_team}")
    #                             print(f"    Stat Value: {player_value}")

    #                             # Optionally, you can also display their profile link
    #                             player_profile_link = player.get('athlete', {}).get('links', [{}])[0].get('href', 'No Profile Link')
    #                             print(f"    Profile Link: {player_profile_link}")
    for season_type, weeks in season_week_ranges.items():
        for week in weeks:
            data = load_json(season_type, week)
            if data:
                for event in data['events']:
                    for competition in event['competitions']:
                        for leader in competition.get('leaders', []):
                            stat_name = leader.get('name', 'Unknown Stat')
                            for player in leader.get('leaders', []):
                                player_name = player.get('athlete', {}).get('displayName', 'Unknown Player')
                                player_team = player.get('athlete', {}).get('team', {}).get('id', 'Unknown Team')
                                player_position = player.get('athlete', {}).get('position', {}).get('abbreviation', 'Unknown Position')
                                player_value = player.get('displayValue', 0)

                                # Add row to output data
                                output_data.append({
                                    'week': week,
                                    'season_type': season_type,
                                    'stat_name': stat_name,
                                    'player_name': player_name,
                                    'team_id': player_team,
                                    'position': player_position,
                                    'stat_value': player_value
                                })
# Write to CSV
    with open('fantasy_stats.csv', 'w', newline='') as csvfile:
        fieldnames = ['week', 'season_type', 'stat_name', 'player_name', 'team_id', 'position', 'stat_value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_data)
generate_csv()


