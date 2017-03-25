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
>>> from selenium import webdriver
```

### Pick a webdriver to use.  I prefer phantomjs.
`>>> driver = webdriver.PhantomJS(service_args=['--load-images=no'])`

### View supported leagues
```
>>> print(espn.get_leagues())
['nfl', 'mlb', 'nba', 'ncf', 'ncb']
```

### Get all scoreboard urls for a league in a given year. It will make one get request to ESPN.com and display the URL
```
>>> scoreboard_urls = espn.get_all_scoreboard_urls("nfl", 2016, driver)
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/1
```

### Save all scoreboard data from these urls in the cached_json_data folder
```
>>> for scoreboard_url in scoreboard_urls:
...     data = espn.get_scoreboard_json(scoreboard_url, driver, cached_json_path="cached_json", cache_json=True, use_cached_json=True)
... 
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/1/week/1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/1/week/2
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/1/week/3
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/1/week/4
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/1/week/5
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/2
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/3
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/4
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/5
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/6
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/7
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/8
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/9
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/10
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/11
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/12
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/13
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/14
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/15
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/16
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/17
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/3/week/1
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/3/week/2
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/3/week/3
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/3/week/4
http://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/3/week/5
```

### Now that this data is saved, we can loop through it quickly to print out postseason scores for example
```
>>> for scoreboard_url in scoreboard_urls:
...     data = espn.get_scoreboard_json(scoreboard_url, driver, cached_json_path="cached_json", cache_json=True, use_cached_json=True)
...     for event in data['events']:
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

### Quit webdriver
`>>> driver.quit()`
