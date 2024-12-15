import espn_scraper as espn
import json


def ppjson(data):
    print(json.dumps(data, indent=2, sort_keys=True))


def get_all_game_ids(league, year):
    scoreboard_urls = espn.get_all_scoreboard_urls(league, year)
    # print(scoreboard_urls)
    game_ids = []
    regular_season_game_ids = []
    post_season_game_ids = []
    pre_season_game_ids = []

    for scoreboard_url in scoreboard_urls:
        try:
            data = espn.get_url(scoreboard_url, cached_path="cached_data")
            # ppjson(data)
            # Try accessing events in the new structure
            events = data.get('events', [])

            # Fallback to old structure if needed
            if not events:
                events = data.get('content', {}).get('sbData', {}).get('events', [])

            # Skip the URL if no events are found
            if not events:
                continue

            # Collect game IDs and categorize by season
            for event in events:
                game_id = event['id']
                
                # Avoid duplicates in the game IDs list
                if game_id not in game_ids:
                    game_ids.append(game_id)

                # Check season type and categorize
                season_type = event.get('season', {}).get('type')
                if season_type == 1:  # Post-season
                    if game_id not in post_season_game_ids:
                        post_season_game_ids.append(game_id)
                elif season_type == 2:  # Regular-season
                    if game_id not in regular_season_game_ids:
                        regular_season_game_ids.append(game_id)
                elif season_type == 3:  # Pre-season
                    if game_id not in pre_season_game_ids:
                        pre_season_game_ids.append(game_id)

        except Exception as e:
            print(f"Error processing URL {scoreboard_url}: {e}")

    return regular_season_game_ids, post_season_game_ids, pre_season_game_ids

# if __name__ == "__main__":
#     reg, post, pre = get_all_game_ids("nfl", 2023)
#     # print(reg)
