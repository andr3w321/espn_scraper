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
    for event in data['content']['sbData']['events']:
        if event['season']['type'] == 3:
            print(event['season']['type'],
                  event['season']['year'],
                  event['competitions'][0]['competitors'][0]['team']['abbreviation'],
                  event['competitions'][0]['competitors'][0]['score'],
                  event['competitions'][0]['competitors'][1]['team']['abbreviation'],
                  event['competitions'][0]['competitors'][1]['score'])

url = espn.get_game_url("boxscore", "nba", 400900498)
json_data = espn.get_url(url)
print(json_data['gamepackageJSON']['boxscore']['teams'][0]['team']['name'])
ppjson(json_data['gamepackageJSON']['boxscore']['teams'][0]['statistics'][0])

url = espn.get_game_url("playbyplay", "ncf", 400868977)
json_data = espn.get_url(url)
print(json_data['gamepackageJSON']['drives']['previous'][0]['plays'][0]['text'])

# a few requests will return a beautiful soup objects instead of json
url = espn.get_game_url("boxscore", "nhl", 400885533)
soup = espn.get_url(url)
away_team = soup.select('.team-info a')[0].text
home_team = soup.select('.team-info a')[1].text
away_score = soup.select('.team-info .gp-awayScore')[0].text
home_score = soup.select('.team-info .gp-homeScore')[0].text
print(away_team, away_score, home_team, home_score)

# you may have better luck parsing their gamecast data for boxscore or playbyplay
gamecast_url = espn.get_game_url("gamecast", "nhl", 400885533)
