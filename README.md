This library will scrape espn.com scoreboards for NFL, MLB, NBA, NCAAF, NCAAB.  It will optionally save the json data for quick lookup later.  All the functions can be found in `espn_scaper/__init__.py`

## Example Usage

### Install espn_scraper
`pip install espn_scraper`

### Make a directory to hold cached scoreboard data
`mkdir cached_json_data`

### Run example.py or open a console to test out
```
$python
>>> import espn_scraper as espn
```

### View supported leagues
```
>>> espn.get_leagues()
['nfl', 'ncf', 'mlb', 'nba', 'ncb', 'ncw', 'wnba']
```

### Get all scoreboard urls for a league in a given year. It will make one get request to ESPN.com and display the URL
```
>>> scoreboard_urls = espn.get_all_scoreboard_urls("nfl", 2016)
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/1?xhr=1
```

### Save all scoreboard data from these urls in the cached_json_data folder
```
>>> for scoreboard_url in scoreboard_urls:
...     data = espn.get_json(scoreboard_url, "scoreboards")
... 
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/1/week/1?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/1/week/2?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/1/week/3?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/1/week/4?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/1/week/5?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/1?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/2?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/3?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/4?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/5?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/6?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/7?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/8?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/9?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/10?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/11?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/12?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/13?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/14?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/15?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/16?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/17?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/3/week/1?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/3/week/2?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/3/week/3?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/3/week/4?xhr=1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/3/week/5?xhr=1
```

### Now that this data is saved, we can loop through it quickly to print out postseason scores for example
```
>>> for scoreboard_url in scoreboard_urls:
...     data = espn.get_json(scoreboard_url, "scoreboards")
...     for event in data['content']['sbData']['events']:
...         if event['season']['type'] == 3:
...             print(event['season']['type'],
...                   event['season']['year'],
...                   event['competitions'][0]['competitors'][0]['team']['abbreviation'],
...                   event['competitions'][0]['competitors'][0]['score'],
...                   event['competitions'][0]['competitors'][1]['team']['abbreviation'],
...                   event['competitions'][0]['competitors'][1]['score'])
... 
3 2016 HOU 27 OAK 14
3 2016 SEA 26 DET 6
3 2016 PIT 30 MIA 12
3 2016 GB 38 NYG 13
3 2016 ATL 36 SEA 20
3 2016 NE 34 HOU 16
3 2016 DAL 31 GB 34
3 2016 KC 16 PIT 18
3 2016 ATL 44 GB 21
3 2016 NE 36 PIT 17
3 2016 NFC 13 AFC 20
3 2016 ATL 28 NE 34
```
