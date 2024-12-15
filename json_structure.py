import json

file_path = "/Users/marcojonsson/FantasyDataScraping/espn_scraper/cached_data/nfl/boxscore/https:||www.espn.com|nfl|boxscore?gameId=401550167&_xhr=1.json"

with open(file_path, "r") as f:
    data = json.load(f)

# Print the top-level keys

import json

# Recursive function to find a key in JSON and return both path and value
def find_key_in_json(json_obj, key, path=None):
    """Recursively search for a key in a nested JSON object and return the path and value."""
    if path is None:
        path = []
    
    # If the current object is a dictionary, check each key-value pair
    if isinstance(json_obj, dict):
        for k, v in json_obj.items():
            if k == key:
                return path + [k], v  # Return the path and the value
            result = find_key_in_json(v, key, path + [k])
            if result:
                return result  # Return the first match found
    
    # If the current object is a list, iterate through each item
    elif isinstance(json_obj, list):
        for idx, item in enumerate(json_obj):
            result = find_key_in_json(item, key, path + [f"[{idx}]"])
            if result:
                return result  # Return the first match found
    
    # If the key is not found, return None
    return None

# Function to find the path of a key in JSON without returning the value
def find_key_path_in_json(json_obj, key, path=None):
    """Recursively search for a key in a nested JSON object and return only the path."""
    if path is None:
        path = []
    
    # If the current object is a dictionary, check each key-value pair
    if isinstance(json_obj, dict):
        for k, v in json_obj.items():
            if k == key:
                return path + [k]  # Return just the path
            result = find_key_path_in_json(v, key, path + [k])
            if result:
                return result  # Return the first match found
    
    # If the current object is a list, iterate through each item
    elif isinstance(json_obj, list):
        for idx, item in enumerate(json_obj):
            result = find_key_path_in_json(item, key, path + [f"[{idx}]"])
            if result:
                return result  # Return the first match found
    
    # If the key is not found, return None
    return None

# Example usage
file_path = "/Users/marcojonsson/FantasyDataScraping/espn_scraper/cached_data/apis/scoreboard/https:||site.api.espn.com|apis|site|v2|sports|football|nfl|scoreboard?dates=2023&seasontype=1&week=1.json"
with open(file_path, "r") as f:
    data = json.load(f)

# Find the gameId path and its value
week_path,week_value = find_key_in_json(data, "week")
if week_path:
    print(f"Week found at path: {' -> '.join(week_path)}")
    print(f"Game ID value: {week_value}")
else:
    print("Game ID not found.")

# Find the gameId path only (without the value)
bxscr_path = find_key_path_in_json(data, "bxscr")
if bxscr_path:
    print(f"bxscr path: {' -> '.join(bxscr_path)}")
else:
    print("bxscr path not found.")
