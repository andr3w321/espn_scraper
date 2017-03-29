import espn_scraper as espn
import json

''' Pretty print json '''
def ppjson(data):
    print(json.dumps(data, indent=2, sort_keys=True))

leagues = espn.get_leagues()
print(leagues)
for league in leagues:
    teams = espn.get_teams(league)
    print(league, len(teams))

scoreboard_urls = espn.get_all_scoreboard_urls("nfl", 2016)
for scoreboard_url in scoreboard_urls:
    data = espn.get_json(scoreboard_url, "scoreboards", cached_json_path="cached_json", cache_json=True, use_cached_json=True)
    for event in data['content']['sbData']['events']:
        if event['season']['type'] == 3:
            print(event['season']['type'],
                  event['season']['year'],
                  event['competitions'][0]['competitors'][0]['team']['abbreviation'],
                  event['competitions'][0]['competitors'][0]['score'],
                  event['competitions'][0]['competitors'][1]['team']['abbreviation'],
                  event['competitions'][0]['competitors'][1]['score'])
