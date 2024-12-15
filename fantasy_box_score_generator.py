from fantasy_football_game_ids import get_all_game_ids
import espn_scraper as espn

def get_box_scores():
    # Fetch game IDs for different seasons
    regular_season_ids, post_season_ids, pre_season_ids = get_all_game_ids("nfl", 2023)
    
    # Combine all game IDs into a single list
    all_game_ids = {
        "Regular Season": regular_season_ids,
        "Post Season": post_season_ids,
        "Pre Season": pre_season_ids,
    }
    
    excluded_game_id = 401616889
    
    # Iterate through game IDs and fetch data while excluding the specified game ID
    for season_type, game_ids in all_game_ids.items():
        for game_id in game_ids:
            # Log the current game ID and type for debugging
            # print(f"Processing game ID: {game_id} (type: {type(game_id)}) from {season_type}")
            
            # Compare game ID against excluded_game_id
            if str(game_id) == str(excluded_game_id):  # Ensure both are strings
                # print(f"Excluding game ID: {game_id} from {season_type}")
                continue  # Skip this game ID
            
            # Fetch and cache data
            data = espn.get_url(f"https://www.espn.com/nfl/boxscore?gameId={game_id}&_xhr=1", "cached_data")
            # print(f"Fetched box score for game ID: {game_id} from {season_type}")

# Call the function to fetch box scores
get_box_scores()
