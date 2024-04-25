import json
import pytz
from dateutil import parser
from dateutil.relativedelta import relativedelta
import datetime
import os.path
import requests
from bs4 import BeautifulSoup
BASE_URL = "https://www.espn.com"
QUERY_STRING = "_xhr=1"
#ESPN seems to be blocking requests with default blank headers
DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
API_v2_BASE_URL = "https://site.api.espn.com/apis/site/v2/sports"

## General functions
def retry_request(url, headers=DEFAULT_HEADERS):
    """Get a url and return the request, try it up to 3 times if it fails initially"""
    session = requests.Session()
    session.mount("http://", requests.adapters.HTTPAdapter(max_retries=3))
    res = session.get(url=url, allow_redirects=True, headers=headers)
    session.close()
    return res

def get_soup(res):
    return BeautifulSoup(res.text, "lxml")

def get_new_json(url, headers=DEFAULT_HEADERS):
    print(url)
    res = retry_request(url, headers)
    if res.status_code == 200:
        return res.json()
    else:
        print("ERROR:", res.status_code)
        return {"error_code": res.status_code, "error_msg": "URL Error"}

def get_new_html_soup(url, headers=DEFAULT_HEADERS):
    print(url)
    res = retry_request(url, headers)
    if res.status_code == 200:
        return get_soup(res)
    else:
        print("ERROR: ESPN", res.status_code)
        return {"error_code": res.status_code, "error_msg": "ESPN Error"}

## Get constants
def get_date_leagues():
    return ["mlb","nba","ncb","ncw","wnba","nhl"]

def longify_league(league):
    if league == "ncb":
        league = "mens-college-basketball"
    elif league == "ncw":
        league = "womens-college-basketball"
    elif league == "ncf":
        league = "college-football"
    return league

def get_week_leagues():
    return ["nfl","ncf"]

def get_ncb_groups():
    return [50,55,56,100]

def get_ncw_groups():
    return [50,55,100]

def get_ncf_groups():
    return [80,81]

def get_leagues():
    """ Return a list of supported leagues """
    return get_week_leagues() + get_date_leagues()

def get_no_scoreboard_json_leagues():
    """ Scoreboard json isn't easily available for some leagues, have to grab the game_ids from sportscenter_api url """
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
def get_sportscenter_api_url(league, dates, sport=None):
    """ Alternative API endpoint """
    if sport == None:
        sport = get_sport(league)
    return "https://sportscenter.api.espn.com/apis/v1/events?sport={}&league={}&dates={}".format(sport, league, dates)

def get_date_scoreboard_url(league, dates, groups=None, sport=None, limit=None):
    """ Return a scoreboard url for a league that uses dates (nonfootball, but function also works for football)"""
    if sport == None:
        sport = get_sport(league)
    league = longify_league(league)
    url = "{}/{}/{}/scoreboard?dates={}".format(API_v2_BASE_URL, sport, league, dates)
    if groups !=None:
        if limit == None:
            limit = 1000
        url+= "&groups={}".format(groups)
    if limit != None:
        url += "&limit={}".format(limit)
    return url

def get_week_scoreboard_url(league, season_year, season_type=None, week=None, groups=None, sport=None):
    """ Return a scoreboard url for a league that uses weeks (football)
    Example urls
    By year: https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?limit=1000&dates=2022
    By year, seasontype, week: https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates=2022&seasontype=2&week=1
    By date range: https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates=20200901-20210228
    By date: https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates=20200901"""

    if sport == None:
        sport = get_sport(league)
    league = longify_league(league)
    url = "{}/{}/{}/scoreboard?dates={}".format(API_v2_BASE_URL, sport, league, season_year)
    if season_type != None:
        url += "&seasontype={}".format(season_type)
    if week != None:
        url += "&week={}".format(week)
    #TODO implement groups?
    return url

def get_game_url(url_type, league, espn_id):
    valid_url_types = ["recap", "boxscore", "playbyplay", "conversation", "gamecast"]
    if url_type not in valid_url_types:
        raise ValueError("Unknown url_type for get_game_url. Valid url_types are {}".format(valid_url_types))
    return "{}/{}/{}?gameId={}&{}".format(BASE_URL, league, url_type, espn_id, QUERY_STRING)

def get_current_scoreboard_urls(league, offset=0):
    """ Return a list of the current scoreboard urls for a league 
    For date leagues optional offset is in days
    For week leagues optional offseet is in weeks """
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

def get_all_scoreboard_urls(league, season_year):
    """ Return a list of all scoreboard urls for a given league and season year """
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

def get_data_type_from_url(url):
    """ Guess and return the data_type based on the url """
    data_type = None
    valid_data_types = ["scoreboard", "recap", "boxscore", "playbyplay", "conversation", "gamecast"]
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

def get_season_start_end_datetimes(league, season_year):
    """ Guess a random date in a leagues season and return its calendar start and end dates, only non football adheres to this format"""
    if league == "mlb":
        return get_season_start_end_datetimes_helper(get_date_scoreboard_url(league, str(season_year) + "0415"))
    elif league == "nba":
        return get_season_start_end_datetimes_helper(get_date_scoreboard_url(league, str(season_year - 1) + "1101"))
    elif league == "ncb" or league == "ncw":
        return get_season_start_end_datetimes_helper(get_date_scoreboard_url(league, str(season_year - 1) + "1130"))
    elif league == "wnba":
        # hardcode wnba start end dates, assumed to be April 20 thru Oct 31
        return datetime.datetime(season_year,4,20, tzinfo=pytz.timezone("US/Eastern")).astimezone(pytz.utc), datetime.datetime(season_year,10,31, tzinfo=pytz.timezone("US/Eastern")).astimezone(pytz.utc)
    elif league == "nhl":
        # hardcode nhl start end dates, assumed to be Oct 1 thru June 30
        return datetime.datetime(season_year-1,10,1, tzinfo=pytz.timezone("US/Eastern")).astimezone(pytz.utc), datetime.datetime(season_year,6,30, tzinfo=pytz.timezone("US/Eastern")).astimezone(pytz.utc)
    else:
        raise ValueError("League must be {} to get season start and end datetimes".format(get_date_leagues()))

def get_filename(cached_json_path, league, data_type, url):
    """ Build a full filename with directories for given league, data_type and url"""
    # add slash if necessary to cached_json_path
    if cached_json_path[-1] != "/":
        cached_json_path += "/"
    dir_path = cached_json_path + "/" + league + "/" + data_type + "/"
    # create a league directory and data_type directory in cached_json if doesn't already exist
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # create filename with / replaced with |
    filename = dir_path + url.replace('/','|')
    ext = ".json"
    if filename.endswith(ext) == False:
        filename = filename + ext
    return filename

def get_cached(filename):
    """ Return cached json if it exists """
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
def get_teams(league):
    """ Returns a list of teams with ids and names """
    teams = []
    if league == "ncf":
        # espn's college football teams page only lists fbs (blank division)
        # need to grab teams from standings page instead if want all the fbs and fcs teams
        for division in ["","fcs-i-aa"]:
            url = BASE_URL + "/college-football/standings/_/view/" + division
            print(url)
            soup = get_soup(retry_request(url))
            selector = ".hide-mobile"
            team_divs = soup.select(selector)
            for team_div in team_divs:
                teams.append({'id': team_div.find("a")['href'].split('/')[-2], 'name': team_div.text})
    else:
        url = BASE_URL + "/" + league + "/teams"
        print(url)
        soup = get_soup(retry_request(url))
        if league == "wnba":
            selector = "div.pl3"
        else:
            selector = "div.mt3"
        team_divs = soup.select(selector)
        for team_div in team_divs:
            teams.append({'id': team_div.find("a")['href'].split('/')[-2], 'name': team_div.find("h2").text})
    return teams

def get_standings(league, season_year, college_division=None):
    standings = {"conferences": {}}
    if league in ["nhl","nfl","mlb","nba","wnba","ncf","ncb","ncw"]:
        if league == "ncf" and college_division == None:
            # default to fbs
            college_division = ""
        if college_division:
            valid_college_divisions = ["fbs", "fcs", "fcs-i-aa", "d2", "d3"]
            if college_division == "fcs":
                college_division = "fcs-i-aa"
            if college_division in valid_college_divisions:
                url = "{}/{}/standings/_/season/{}/view/{}".format(BASE_URL, league, season_year, college_division)
            else:
                raise ValueError("College division must be none or {}".format(",".join(valid_college_divisions)))
        elif league in ["wnba"]:
            url = "{}/{}/standings/_/season/{}/group/conference".format(BASE_URL, league, season_year)
        else:
            url = "{}/{}/standings/_/season/{}/group/division".format(BASE_URL, league, season_year)

        print(url)
        soup = get_soup(retry_request(url))
        standings_divs = soup.find_all("div", class_="standings__table")

        for i in range(len(standings_divs)):
            conference_name = standings_divs[i].find("div", class_="Table__Title").text
            standings["conferences"][conference_name] = {"divisions": {}}
            division = "" # default blank division name
            teams_table = standings_divs[i].find("table", class_="Table--fixed-left")
            trs = teams_table.find_all("tr")
            for tr in trs:
                if "subgroup-headers" in tr["class"]:
                    division = tr.text # replace default blank division name
                    standings["conferences"][conference_name]["divisions"][division] = {"teams": []}
                elif tr.text != "":
                    if division == "" and standings["conferences"][conference_name]["divisions"] == {}:
                        standings["conferences"][conference_name]["divisions"][division] = {"teams": []}
                    team = {}
                    team_span_tag = tr.find("td", class_="Table__TD").find("span", class_="hide-mobile")
                    team_a_tag = team_span_tag.find("a")
                    if team_a_tag is None:
                        # some teams are now defunct with no espn links
                        team["name"] = team_span_tag.text.strip()
                        team["abbr"] = ""
                    else:
                        team["name"] = team_a_tag.text
                        if league in ["ncf","ncb","ncw"]:
                            team["abbr"] = team_a_tag["href"].split("/id/")[1].split("/")[0].upper()
                        else:
                            team["abbr"] = team_a_tag["href"].split("/name/")[1].split("/")[0].upper()
                    standings["conferences"][conference_name]["divisions"][division]["teams"].append(team)

    return standings
                
def get_calendar(league, date_or_season_year):
    """ Return a calendar for a league and season_year"""
    if league in get_week_leagues():
        url = get_week_scoreboard_url(league, date_or_season_year, 2, 1)
    elif league in get_date_leagues():
        url = get_date_scoreboard_url(league, date_or_season_year)
    # TODO use cached replies for older urls
    return get_url(url)['leagues'][0]['calendar']

def get_url(url, cached_path=None):
    """ Retrieve an ESPN JSON data or HTML BeautifulSoup, either from cache or make new request """
    data_type = get_data_type_from_url(url)
    league = get_league_from_url(url)
    """
    if data_type == "scoreboard":
        # for wnba and nhl we'll use a different api to retrieve game_ids and basic game data
        if league in get_no_scoreboard_json_leagues():
            url = get_sportscenter_api_url(get_sport(league), league, get_date_from_scoreboard_url(url))
    """
    return get_cached_url(url, league, data_type, cached_path)

def get_cached_url(url, league, data_type, cached_path, headers=DEFAULT_HEADERS):
    """ get_url helper if want to specify the league and datatype (for non espn.com links) """
    if cached_path:
        filename = get_filename(cached_path, league, data_type, url)
        data = get_cached(filename)
    else:
        data = None
    if data == None:
        ext = "json"
        data = get_new_json(url, headers)
        # dont cache if got an ESPN internal 500 error
        if cached_path and "error_code" not in data:
            with open(filename, 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
    return data

