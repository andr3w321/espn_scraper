import espn_scraper as espn
import json

''' Pretty print json helper '''
def ppjson(data):
    print(json.dumps(data, indent=2, sort_keys=True))

leagues = espn.get_leagues()
print(leagues)
for league in leagues:
    teams = espn.get_teams(league)
    print(league, len(teams))

# print nfl 2016 postseason scores
scoreboard_urls = espn.get_all_scoreboard_urls("nfl", 2016)
for scoreboard_url in scoreboard_urls:
    data = espn.get_url(scoreboard_url, cached_path="cached_json")
    for event in data['events']:
        if event['season']['type'] == 3:
            print(event['season']['type'],
                  event['season']['year'],
                  event['competitions'][0]['competitors'][0]['team']['abbreviation'],
                  event['competitions'][0]['competitors'][0]['score'],
                  event['competitions'][0]['competitors'][1]['team']['abbreviation'],
                  event['competitions'][0]['competitors'][1]['score'])

url = espn.get_game_url("boxscore", "nba", 400900498)
json_data = espn.get_url(url)
#ppjson(json_data) # print full long json

print(json_data['page']['content']['gamepackage']['bxscr'][0]['tm']['dspNm'])
ppjson(json_data['page']['content']['gamepackage']['bxscr'][0]['stats'][0])

url = espn.get_game_url("playbyplay", "ncf", 400868977)
json_data = espn.get_url(url)
for play_number, play in enumerate(json_data['page']['content']['gamepackage']['allPlys']):
    if 'headline' not in play:
        continue
    print(play_number, play['teamName'], play['headline'], play['description'])


# NHL example
url = espn.get_game_url("boxscore", "nhl", 400885533)
json_data = espn.get_url(url)
away_team = json_data['page']['content']['gamepackage']['bxscr'][0]['tm']['abbrev']
home_team = json_data['page']['content']['gamepackage']['bxscr'][1]['tm']['abbrev']
away_score = json_data['page']['content']['gamepackage']['scrSumm']['lnscrs']['awy'][3]
home_score = json_data['page']['content']['gamepackage']['scrSumm']['lnscrs']['hme'][3]
print(away_team, away_score, home_team, home_score)
