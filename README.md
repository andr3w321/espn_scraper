This library will scrape espn.com scoreboards, boxscores, playbyplays for most sports NFL, MLB, NBA, NCAAF, NCAAB, NCAAW, WNBA, NHL.  It will optionally save the data for quick lookup later.  All the functions can be found in `espn_scaper/__init__.py`  Some example usage can be found in example.py or the below README

## Example Usage

Install espn_scraper

`pip install espn_scraper`

Import the package

`>>> import espn_scraper as espn`

To view supported leagues
```
>>> espn.get_leagues()
['nfl', 'ncf', 'mlb', 'nba', 'ncb', 'ncw', 'wnba', 'nhl']
```

Before retrieving ESPN data, let's write a pretty json printer function
```
import json
def ppjson(data):
    print(json.dumps(data, indent=2, sort_keys=True))
```

Now let's use it print the current NFL team names and their abbreviations
```
>>> ppjson(espn.get_teams("nfl"))
https://www.espn.com/nfl/teams
[
  {
    "id": "buf",
    "name": "Buffalo Bills"
  },
  {
    "id": "mia",
    "name": "Miami Dolphins"
  },
  {
    "id": "ne",
    "name": "New England Patriots"
  },
  {
    "id": "nyj",
    "name": "New York Jets"
  },
  {
    "id": "bal",
    "name": "Baltimore Ravens"
  },
  {
    "id": "cin",
    "name": "Cincinnati Bengals"
  },
  {
    "id": "cle",
    "name": "Cleveland Browns"
  },
  {
    "id": "pit",
    "name": "Pittsburgh Steelers"
  },
  {
    "id": "hou",
    "name": "Houston Texans"
  },
  {
    "id": "ind",
    "name": "Indianapolis Colts"
  },
  {
    "id": "jax",
    "name": "Jacksonville Jaguars"
  },
  {
    "id": "ten",
    "name": "Tennessee Titans"
  },
  {
    "id": "den",
    "name": "Denver Broncos"
  },
  {
    "id": "kc",
    "name": "Kansas City Chiefs"
  },
  {
    "id": "lac",
    "name": "Los Angeles Chargers"
  },
  {
    "id": "oak",
    "name": "Oakland Raiders"
  },
  {
    "id": "dal",
    "name": "Dallas Cowboys"
  },
  {
    "id": "nyg",
    "name": "New York Giants"
  },
  {
    "id": "phi",
    "name": "Philadelphia Eagles"
  },
  {
    "id": "wsh",
    "name": "Washington Redskins"
  },
  {
    "id": "chi",
    "name": "Chicago Bears"
  },
  {
    "id": "det",
    "name": "Detroit Lions"
  },
  {
    "id": "gb",
    "name": "Green Bay Packers"
  },
  {
    "id": "min",
    "name": "Minnesota Vikings"
  },
  {
    "id": "atl",
    "name": "Atlanta Falcons"
  },
  {
    "id": "car",
    "name": "Carolina Panthers"
  },
  {
    "id": "no",
    "name": "New Orleans Saints"
  },
  {
    "id": "tb",
    "name": "Tampa Bay Buccaneers"
  },
  {
    "id": "ari",
    "name": "Arizona Cardinals"
  },
  {
    "id": "lar",
    "name": "Los Angeles Rams"
  },
  {
    "id": "sf",
    "name": "San Francisco 49ers"
  },
  {
    "id": "sea",
    "name": "Seattle Seahawks"
  }
]
```

To get the teams and their abbreviations for an old season_year use the get_standings(league, season_year) function. For example see the old NBA divisions from 2004 including the Seattle Supersonics
```
>>> ppjson(espn.get_standings("nba", 2004))
https://www.espn.com/nba/standings/_/season/2004/group/division
{
  "conferences": {
    "Eastern Conference": {
      "divisions": {
        "Atlantic": {
          "teams": [
            {
              "abbr": "",
              "name": "New Jersey Nets"
            },
            {
              "abbr": "MIA",
              "name": "Miami Heat"
            },
            {
              "abbr": "NY",
              "name": "New York Knicks"
            },
            {
              "abbr": "BOS",
              "name": "Boston Celtics"
            },
            {
              "abbr": "PHI",
              "name": "Philadelphia 76ers"
            },
            {
              "abbr": "WSH",
              "name": "Washington Wizards"
            },
            {
              "abbr": "ORL",
              "name": "Orlando Magic"
            }
          ]
        },
        "Central": {
          "teams": [
            {
              "abbr": "IND",
              "name": "Indiana Pacers"
            },
            {
              "abbr": "DET",
              "name": "Detroit Pistons"
            },
            {
              "abbr": "",
              "name": "New Orleans Hornets"
            },
            {
              "abbr": "MIL",
              "name": "Milwaukee Bucks"
            },
            {
              "abbr": "CLE",
              "name": "Cleveland Cavaliers"
            },
            {
              "abbr": "TOR",
              "name": "Toronto Raptors"
            },
            {
              "abbr": "ATL",
              "name": "Atlanta Hawks"
            },
            {
              "abbr": "CHI",
              "name": "Chicago Bulls"
            }
          ]
        },
        "Southeast": {
          "teams": []
        }
      }
    },
    "Western Conference": {
      "divisions": {
        "Midwest": {
          "teams": [
            {
              "abbr": "MIN",
              "name": "Minnesota Timberwolves"
            },
            {
              "abbr": "SA",
              "name": "San Antonio Spurs"
            },
            {
              "abbr": "DAL",
              "name": "Dallas Mavericks"
            },
            {
              "abbr": "MEM",
              "name": "Memphis Grizzlies"
            },
            {
              "abbr": "HOU",
              "name": "Houston Rockets"
            },
            {
              "abbr": "DEN",
              "name": "Denver Nuggets"
            },
            {
              "abbr": "UTAH",
              "name": "Utah Jazz"
            }
          ]
        },
        "Pacific": {
          "teams": [
            {
              "abbr": "LAL",
              "name": "Los Angeles Lakers"
            },
            {
              "abbr": "SAC",
              "name": "Sacramento Kings"
            },
            {
              "abbr": "POR",
              "name": "Portland Trail Blazers"
            },
            {
              "abbr": "GS",
              "name": "Golden State Warriors"
            },
            {
              "abbr": "",
              "name": "Seattle SuperSonics"
            },
            {
              "abbr": "PHX",
              "name": "Phoenix Suns"
            },
            {
              "abbr": "LAC",
              "name": "LA Clippers"
            }
          ]
        }
      }
    }
  }
}
```

Espn json data can usually be found by appending "&xhr=1" to the urls. For example, the html for the recent NFL playoff game is 

https://www.espn.com/nfl/boxscore?gameId=401131040 and the json link is

https://www.espn.com/nfl/boxscore?gameId=401131040&xhr=1

To retrieve the json data we can run
```
>>> espn.get_url("https://www.espn.com/nfl/boxscore?gameId=401131040&xhr=1")
https://www.espn.com/nfl/boxscore?gameId=401131040&xhr=1
{'gameId': 401131040, 'DTCpackages': {'p...
```

You'll notice that the url retrieved was printed to console. This means espn_scraper hit espn.com with a request. If you'll be making many of these requests to parse the data, it's best to download the data.

First make a directory to hold cached data
`mkdir cached_data`

Pass the cached_data folder link to the espn.get_url( as an argument
```
>>> data = espn.get_url("https://www.espn.com/nfl/boxscore?gameId=401131040&xhr=1", "cached_data")
https://www.espn.com/nfl/boxscore?gameId=401131040&xhr=1
```

This json is now stored locally
```
$ ls cached_data/nfl/boxscore/
'https:||www.espn.com|nfl|boxscore?gameId=401131040&xhr=1.json'
```

In future requests, if we query this same boxscore, it will be done locally via the saved json file, as long as we pass the cached data folder to the request
```
>>> data = espn.get_url("https://www.espn.com/nfl/boxscore?gameId=401131040&xhr=1", "cached_data")
>>>
```

Notice that no url is printed after the request, indicating that no requests were made to any outside urls.

If you know the espn game id you can get the JSON recap, boxscore, playbyplay, conversation, or gamecast data. Eg

```
>>> for data_type in ["recap", "boxscore", "playbyplay", "conversation" or "gamecast"]:
...     url = espn.get_game_url(data_type, "nfl", 401131040)
...     data = espn.get_url(url)
... 
https://www.espn.com/nfl/recap?gameId=401131040&xhr=1
https://www.espn.com/nfl/boxscore?gameId=401131040&xhr=1
https://www.espn.com/nfl/playbyplay?gameId=401131040&xhr=1
https://www.espn.com/nfl/conversation?gameId=401131040&xhr=1
```

If you want to get all the game ids for a season you'll can use the get_all_scoreboard_urls(league, season_year) function
```
>>> espn.get_all_scoreboard_urls("nba", 2016)
https://www.espn.com/nba/scoreboard/_/date/20151101?xhr=1
['https://www.espn.com/nba/scoreboard/_/date/20151001?xhr=1', 'https://www.espn.com/nba/scoreboard/_/date/20151002?xhr=1', 'https://www.espn.com/nba/scoreboard/_/date/20151003?xhr=1', 'https://www.espn.com/nba/scoreboard/_/date/20151004?xhr=1', 'https://www.espn.com/nba/scoreboard/_/date/20...
```

You can then get all the espn game_ids for a season by parsing the events for each scoreboard url
```
>>> game_ids = []
>>> for scoreboard_url in scoreboard_urls:
...   data = espn.get_url(scoreboard_url, cached_path="cached_data")
...   for event in data['content']['sbData']['events']:
...       if event['id'] not in game_ids:
...           game_ids.append(event['id'])
... 
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/1/week/1?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/1/week/2?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/1/week/3?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/1/week/4?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/1/week/5?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/1?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/2?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/3?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/4?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/5?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/6?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/7?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/8?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/9?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/10?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/11?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/12?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/13?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/14?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/15?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/16?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/2/week/17?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/3/week/1?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/3/week/2?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/3/week/3?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/3/week/4?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/3/week/5?xhr=1
https://www.espn.com/nfl/scoreboard/_/year/2016/seasontype/4/week/1?xhr=1
>>> print(game_ids)
['400868831', '400874795', '400874854',...
```
