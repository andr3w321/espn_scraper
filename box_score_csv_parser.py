
import os
import json
import csv

# Specify directory containing JSON files and output CSV file
input_directory = "/Users/marcojonsson/FantasyDataScraping/espn_scraper/cached_data/nfl/boxscore/"
output_csv = "nfl_player_stats.csv"

# Define the desired stats and their corresponding keys
desired_keys = {
    
    
    "passing":[
        "completions/passingAttempts", "passingYards", "yardsPerPassAttempt",
        "passingTouchdowns", "interceptions", "sacks-sackYardsLost", "adjQBR", "QBRating"
    ],
    "rushing":[
        "rushingAttempts", "rushingYards", "yardsPerRushAttempt",
        "rushingTouchdowns", "longRushing"
    ],
    "receiving":[
        "receptions","receivingYards","yardsPerReception","receivingTouchdowns","longReception","receivingTargets"
    ],
    "fumbles":[
        "fumbles","fumblesLost","fumblesRecovered"
    ],
    "defensive":[
        'totalTackles', 'soloTackles', 'sacks', 'tacklesForLoss', 'passesDefended', 'QBHits', 'defensiveTouchdowns'
    ],
    "interceptions":[
        'interceptions', 'interceptionYards', 'interceptionTouchdowns'
    ],
    "kickReturns":[
        'kickReturns', 'kickReturnYards', 'yardsPerKickReturn', 'longKickReturn', 'kickReturnTouchdowns'
    ],
    "puntReturns":[
        'puntReturns', 'puntReturnYards', 'yardsPerPuntReturn', 'longPuntReturn', 'puntReturnTouchdowns'
    ],
    "kicking":[
        'fieldGoalsMade/fieldGoalAttempts', 'fieldGoalPct', 'longFieldGoalMade', 'extraPointsMade/extraPointAttempts', 'totalKickingPoints'
    ],
    "punting":[
        'punts', 'puntYards', 'grossAvgPuntYards', 'touchbacks', 'puntsInside20', 'longPunt'
    ],
    

    # Add more categories like "receiving" or "defense" as needed
}

# Infer position based on statType
position_by_stat_type = {
    "passing": "QB",
    "rushing": "RB",
    "receiving": "WR",
    "fumbles": "Offensive Player",
    "defensive": "Defender",
    "interceptions": "Defender",
    "kickReturns": "KR",
    "puntReturns": "PR",
    "kicking": "K",
    "punting": "P",
}


flat_desired_keys = [key for category in desired_keys.values() for key in category]
# print(flat_desired_keys)

# Open the CSV file for writing
with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    
    # Write header row
    header = ["GameID","PlayerID", "PlayerName", "Team", "Position", "StatType"] + flat_desired_keys
    writer.writerow(header)

    # Iterate through JSON files in the directory
    count = 0
    for file_name in os.listdir(input_directory):
        if file_name.endswith(".json"):
            # print(file_name)
            file_path = os.path.join(input_directory, file_name)
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                # print("type of data", type(data))
                
                
                # Traverse to the relevant part of the JSON structure
                # Extract Game ID
                game_id = data.get("routing", {}).get("location", {}).get("params", {}).get("gameId")
                # print(f"Extracted Game ID: {game_id}")
                bxscr = data.get("page", {}).get("content",{}).get("gamepackage",{}).get("bxscr")
                # print(type(bxscr))
                                    # Check if `bxscr` exists
                if not bxscr or not isinstance(bxscr, list):
                    # print(f"Skipping {file_name}: 'bxscr' is missing or not a list.")
                    continue
                for team_idx in range(2):  # Two teams: 0 and 1
                    team_name = bxscr[team_idx].get("tm", {}).get("abbrev")
                    
                    for stat_idx, stat_type in enumerate(desired_keys.keys()):
                        athletes = bxscr[team_idx]["stats"][stat_idx]["athlts"]
                        keys_to_zip = bxscr[team_idx]["stats"][stat_idx]["keys"]
                        for athlete in athletes:
                            player_name = athlete["athlt"]["dspNm"]
                            player_id = athlete["athlt"]["id"]  # Extract the player's ID
                            # position = athlete["athlt"].get("pos", "Unknown")
                            position = position_by_stat_type.get(stat_type, "Unknown")
                            stat_vals = athlete["stats"]
                            
                            # Create a stats dictionary and fill missing stats with 0
                            stats_dict = dict(zip(keys_to_zip, stat_vals))
                            filled_stats = [stats_dict.get(key, 0) for key in flat_desired_keys]
                            
                            # Write the row to the CSV
                            row = [game_id, player_id, player_name, team_name, position, stat_type] + filled_stats
                            writer.writerow(row)

print(f"CSV written to {output_csv}")

