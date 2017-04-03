import json
import pytz
from dateutil import parser
from dateutil.relativedelta import relativedelta
import datetime
import os.path
import requests
from bs4 import BeautifulSoup
BASE_URL = "http://www.espn.com"

## General functions
''' Get a url and return the request, try it up to 3 times if it fails initially'''
def retry_request(url):
    session = requests.Session()
    session.mount("http://", requests.adapters.HTTPAdapter(max_retries=3))
    res = session.get(url=url)
    session.close()
    return res

def get_soup(res):
    return BeautifulSoup(res.text, "lxml")

def get_new_json(url):
    print(url)
    return retry_request(url).json()

def get_new_html_soup(url):
    print(url)
    return get_soup(retry_request(url))

## Get constants
def get_date_leagues():
    return ["mlb","nba","ncb","ncw","wnba","nhl"]

def get_week_leagues():
    return ["nfl","ncf"]

def get_ncb_groups():
    return [50,55,56,100]

def get_ncw_groups():
    return [50,55,100]

def get_ncf_groups():
    return [80,81]

''' Return a list of supported leagues '''
def get_leagues():
    return get_week_leagues() + get_date_leagues()

def get_html_boxscore_leagues():
    return ["wnba", "mlb", "nhl"]

''' Scoreboard json isn't easily available for some leagues, have to grab the game_ids from sportscenter_api url '''
def get_no_scoreboard_json_leagues():
    return ["wnba", "nhl"]

def get_sport(league):
    if league in ["nba","wnba","ncb","ncw"]:
        return "basketball"
    elif league in ["mlb"]:
        return "baseball"
    elif league in ["nfl","ncf"]:
        return "football"
    elif league in ["nhl"]:
        return "hockey"

## Get urls
def get_sportscenter_api_url(sport, league, dates):
    return "http://sportscenter.api.espn.com/apis/v1/events?sport={}&league={}&dates={}".format(sport, league, dates)

''' Return a scoreboard url for a league that uses dates (nonfootball)'''
def get_date_scoreboard_url(league, date, group=None):
    if league in get_date_leagues():
        if league == "nhl":
            return "{}/{}/scoreboard?date={}".format(BASE_URL, league, date)
        else:
            if group == None:
                return "{}/{}/scoreboard/_/date/{}?xhr=1".format(BASE_URL, league, date)
            else:
                return "{}/{}/scoreboard/_/group/{}/date/{}?xhr=1".format(BASE_URL, league, group, date)
    else:
        raise ValueError("League must be {} to get date scoreboard url".format(get_date_leagues()))

''' Return a scoreboard url for a league that uses weeks (football)'''
def get_week_scoreboard_url(league, season_year, season_type, week, group=None):
    if league in get_week_leagues():
        if group == None:
            return "{}/{}/scoreboard/_/year/{}/seasontype/{}/week/{}?xhr=1".format(BASE_URL, league, season_year, season_type, week)
        else:
            return "{}/{}/scoreboard/_/group/{}/year/{}/seasontype/{}/week/{}?xhr=1".format(BASE_URL, league, group, season_year, season_type, week)
    else:
        raise ValueError("League must be {} to get week scoreboard url".format(get_week_leagues()))

def get_game_url(url_type, league, espn_id):
    valid_url_types = ["summary", "recap", "boxscore", "playbyplay", "conversation", "gamecast"]
    if url_type not in valid_url_types:
        raise ValueError("Unknown url_type for get_game_url. Valid url_types are {}".format(valid_url_types))
    return "{}/{}/{}?gameId={}&xhr=1".format(BASE_URL, league, url_type, espn_id)

''' Return a list of the current scoreboard urls for a league 
For date leagues optional offset is in days
For week leagues optional offseet is in weeks '''
def get_current_scoreboard_urls(league, offset=0):
    urls = []
    if league in get_date_leagues():
        date_str = (datetime.datetime.now() + relativedelta(days=+offset)).strftime("%Y%m%d")
        if league == "ncb":
            for group in get_ncb_groups():
                urls.append(get_date_scoreboard_url(league, date_str, group))
        elif league == "ncw":
            for group in get_ncw_groups():
                urls.append(get_date_scoreboard_url(league, date_str, group))
        else:
            urls.append(get_date_scoreboard_url(league, date_str))
        return urls
    elif league in get_week_leagues():
        # need to add timezone to now to compare with timezoned entry datetimes later
        dt = datetime.datetime.now(pytz.utc) + relativedelta(weeks=+offset)
        # guess the league season_year
        if dt.month > 2:
            guessed_season_year = dt.year
        else:
            guessed_season_year = dt.year - 1
        calendar = get_calendar(league, guessed_season_year)
        for season_type in calendar:
            if 'entries' in season_type:
                for entry in season_type['entries']:
                    if dt >= parser.parse(entry['startDate']) and dt <= parser.parse(entry['endDate']):
                        if league == "ncf":
                            for group in get_ncf_groups():
                                urls.append(get_week_scoreboard_url(league, guessed_season_year, season_type['value'], entry['value'], group))
                        else:
                            urls.append(get_week_scoreboard_url(league, guessed_season_year, season_type['value'], entry['value']))
        return urls
    else:
        raise ValueError("Unknown league for get_current_scoreboard_urls")

''' Return a list of all scoreboard urls for a given league and season year '''
def get_all_scoreboard_urls(league, season_year):
    urls = []
    if league in get_date_leagues():
        start_datetime, end_datetime = get_season_start_end_datetimes(league, season_year)
        while start_datetime < end_datetime:
            if league == "ncb":
                for group in get_ncb_groups():
                    urls.append(get_date_scoreboard_url(league, start_datetime.strftime("%Y%m%d"), group))
            elif league == "ncw":
                for group in get_ncw_groups():
                    urls.append(get_date_scoreboard_url(league, start_datetime.strftime("%Y%m%d"), group))
            else:
                urls.append(get_date_scoreboard_url(league, start_datetime.strftime("%Y%m%d")))
            start_datetime += relativedelta(days=+1)
        return urls
    elif league in get_week_leagues():
        calendar = get_calendar(league, season_year)
        for season_type in calendar:
            if 'entries' in season_type:
                for entry in season_type['entries']:
                    if league == "ncf":
                        for group in get_ncf_groups():
                            urls.append(get_week_scoreboard_url(league, season_year, season_type['value'], entry['value'], group))
                    else:
                        urls.append(get_week_scoreboard_url(league, season_year, season_type['value'], entry['value']))
        return urls
    else:
        raise ValueError("Unknown league for get_all_scoreboard_urls")

## Get stuff from URL or filenames
def get_league_from_url(url):
    return url.split('.com/')[1].split('/')[0]

def get_date_from_scoreboard_url(url):
    league = get_league_from_url(url)
    if league == "nhl":
        return url.split("?date=")[1].split("&")[0]
    else:
        return url.split('/')[-1].split('?')[0]

''' Guess and return the data_type based on the url '''
def get_data_type_from_url(url):
    data_type = None
    valid_data_types = ["scoreboard", "summary", "recap", "boxscore", "playbyplay", "conversation", "gamecast"]
    for valid_data_type in valid_data_types:
        if valid_data_type in url:
            data_type = valid_data_type
            break
    if data_type == None:
        raise ValueError("Unknown data_type for url. Url must contain one of {}".format(valid_data_types))
    return data_type

def get_filename_ext(filename):
    if filename.endswith(".json"):
        return "json"
    elif filename.endswith(".html"):
        return "html"
    else:
        raise ValueError("Uknown filename extension for {}".format(filename))

## Get requests helpers
def get_season_start_end_datetimes_helper(url):
    # TODO use cached replies if scoreboard url is older than 1 year
    scoreboard = get_url(url)
    return parser.parse(scoreboard['content']['sbData']['leagues'][0]['calendarStartDate']), parser.parse(scoreboard['content']['sbData']['leagues'][0]['calendarEndDate'])

''' Guess a random date in a leagues season and return its calendar start and end dates, only non football adheres to this format'''
def get_season_start_end_datetimes(league, season_year):
    if league == "mlb":
        return get_season_start_end_datetimes_helper(get_date_scoreboard_url(league, str(season_year) + "0415"))
    elif league == "nba":
        return get_season_start_end_datetimes_helper(get_date_scoreboard_url(league, str(season_year - 1) + "1101"))
    elif league == "ncb" or league == "ncw":
        return get_season_start_end_datetimes_helper(get_date_scoreboard_url(league, str(season_year - 1) + "1130"))
    elif league == "wnba":
        # hardcode wnba start end dates, assumed to be May 1 thru Oct 31
        return datetime.datetime(season_year,5,1, tzinfo=pytz.timezone("US/Eastern")).astimezone(pytz.utc), datetime.datetime(season_year,10,31, tzinfo=pytz.timezone("US/Eastern")).astimezone(pytz.utc)
    elif league == "nhl":
        # hardcode nhl start end dates, assumed to be Oct 1 thru June 30
        return datetime.datetime(season_year-1,10,1, tzinfo=pytz.timezone("US/Eastern")).astimezone(pytz.utc), datetime.datetime(season_year,6,30, tzinfo=pytz.timezone("US/Eastern")).astimezone(pytz.utc)
    else:
        raise ValueError("League must be {} to get season start and end datetimes".format(get_date_leagues()))

''' Get a filename extension (either .html or .json depending on league and data_type) '''
def create_filename_ext(league, data_type):
    if league in get_html_boxscore_leagues() and data_type != "scoreboard":
        return "html"
    else:
        return "json"

''' Build a full filename with directories for given league, data_type and url'''
def get_filename(cached_json_path, league, data_type, url):
    # add slash if necessary to cached_json_path
    if cached_json_path[-1] != "/":
        cached_json_path += "/"
    dir_path = cached_json_path + "/" + league + "/" + data_type + "/"
    # create a league directory and data_type directory in cached_json if doesn't already exist
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # create filename with / replaced with |
    return dir_path + url.replace('/','|') + "." + create_filename_ext(league, data_type)

''' Return cached json if it exists '''
def get_cached(filename):
    data = None
    if os.path.isfile(filename):
        ext = get_filename_ext(filename)
        if ext == "json":
            with open(filename) as json_data:
                data = json.load(json_data)
        elif ext == "html":
            data = BeautifulSoup(open(filename), "lxml") 
    return data

## Get requests
''' Returns a list of teams with ids and names '''
def get_teams(league):
    soup = get_soup(retry_request(BASE_URL + "/" + league + "/teams"))
    if league == "wnba":
        selector = "b a"
    else:
        selector = "a.bi"
    team_links = soup.select(selector)
    teams = []
    for team_link in team_links:
        teams.append({'id': team_link['href'].split('/')[-2], 'name': team_link.text})
    return teams

''' Return a calendar for a league and season_year'''
def get_calendar(league, date_or_season_year):
    if league in get_week_leagues():
        url = get_week_scoreboard_url(league, date_or_season_year, 2, 1)
    elif league in get_date_leagues():
        url = get_date_scoreboard_url(league, date_or_season_year)
    # TODO use cached replies for older urls
    return get_url(url)['content']['calendar']

''' Retrieve an ESPN JSON data or HTML BeautifulSoup, either from cache or make new request '''
def get_url(url, cached_path=None):
    data_type = get_data_type_from_url(url)
    league = get_league_from_url(url)
    if data_type == "scoreboard":
        # for wnba and nhl we'll use a different api to retrieve game_ids and basic game data
        if league in get_no_scoreboard_json_leagues():
            url = get_sportscenter_api_url(get_sport(league), league, get_date_from_scoreboard_url(url))
    if cached_path:
        filename = get_filename(cached_path, league, data_type, url)
        data = get_cached(filename)
    else:
        data = None
    if data == None:
        ext = create_filename_ext(league, data_type)
        if ext == "json":
            data = get_new_json(url)
            if cached_path:
                with open(filename, 'w') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
        elif ext == "html":
            data = get_new_html_soup(url)
            if cached_path:
                with open(filename, 'w') as f:
                    f.write(data.prettify())
    return data

