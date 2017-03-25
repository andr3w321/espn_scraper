import re
import json
import pytz
from dateutil import parser
from dateutil.relativedelta import relativedelta
import datetime
import os.path
BASE_URL = "http://www.espn.com"
DATE_LEAGUES = ["mlb","nba","ncb","wcb","wnba"]
WEEK_LEAGUES = ["nfl","ncf"]
NCB_GROUPS = [50,55,56,100]
WCB_GROUPS = [50,55,100]

''' Return a list of supported leagues '''
def get_leagues():
    return ["nfl","mlb","nba","ncf","ncb","wcb","wnba"]

''' Returns a list of teams with ids and names '''
def get_teams(league, driver):
    if league == "wcb":
        league = "womens-college-basketball"
    driver.get(BASE_URL + "/" + league + "/teams")
    if league == "wnba":
        selector = "b a"
    else:
        selector = "a.bi"
    team_links = driver.find_elements_by_css_selector(selector)
    teams = []
    for team_link in team_links:
        teams.append({'id': team_link.get_attribute('href').split('/')[-2], 'name': team_link.text})
    return teams

''' Return a scoreboard url for a league that uses dates (nonfootball)'''
def get_date_scoreboard_url(league, date, group=None):
    if group == None:
        return BASE_URL + "/" + league + "/scoreboard/_/date/" + date
    else:
        return BASE_URL + "/" + league + "/scoreboard/_/group/" + str(group) + "/date/" + date

''' Return a scoreboard url for a league that uses weeks (football)'''
def get_week_scoreboard_url(league, season_year, seasontype, week):
    return BASE_URL + "/" + league + "/scoreboard/_/year/" + str(season_year) + "/seasontype/" + str(seasontype) + "/week/" + str(week)

''' Return a list of the current scoreboard urls for a league 
For date leagues optional offset is in days
For week leagues optional offseet is in weeks '''
def get_current_scoreboard_urls(league, driver, offset=0):
    urls = []
    if league in DATE_LEAGUES:
        date_str = (datetime.datetime.now() + relativedelta(days=+offset)).strftime("%Y%m%d")
        if league == "ncb":
            for group in NCB_GROUPS:
                urls.append(get_date_scoreboard_url(league, date_str, group))
        elif league == "wcb":
            for group in WCB_GROUPS:
                urls.append(get_date_scoreboard_url(league, date_str, group))
        else:
            urls.append(get_date_scoreboard_url(league, date_str))
        return urls
    elif league in WEEK_LEAGUES:
        # need to add timezone to now to compare with timezoned entry datetimes later
        dt = datetime.datetime.now(pytz.utc) + relativedelta(weeks=+offset)
        # guess the league season_year
        if dt.month > 2:
            guessed_season_year = dt.year
        else:
            guessed_season_year = dt.year - 1
        calendar_list = get_calendar_list(league, guessed_season_year, driver)
        for season_type in calendar_list:
            if 'entries' in season_type:
                for entry in season_type['entries']:
                    if dt >= parser.parse(entry['startDate']) and dt <= parser.parse(entry['endDate']):
                        urls.append(get_week_scoreboard_url(league, guessed_season_year, season_type['value'], entry['value']))
        return urls
    else:
        raise ValueError("Unknown league for get_current_scoreboard_urls")

''' Return a list of all scoreboard urls for a given league and season year '''
def get_all_scoreboard_urls(league, season_year, driver):
    urls = []
    if league in DATE_LEAGUES:
        start_end_datetimes = get_season_start_end_datetimes(league, season_year, driver)
        start_datetime = parser.parse(start_end_datetimes['calendarStartDate'])
        end_datetime = parser.parse(start_end_datetimes['calendarEndDate'])
        while start_datetime < end_datetime:
            if league == "ncb":
                for group in NCB_GROUPS:
                    urls.append(get_date_scoreboard_url(league, start_datetime.strftime("%Y%m%d"), group))
            else:
                urls.append(get_date_scoreboard_url(league, start_datetime.strftime("%Y%m%d")))
            start_datetime += relativedelta(days=+1)
        return urls
    elif league in WEEK_LEAGUES:
        calendar_list = get_calendar_list(league, season_year, driver)
        for season_type in calendar_list:
            if 'entries' in season_type:
                for entry in season_type['entries']:
                    urls.append(get_week_scoreboard_url(league, season_year, season_type['value'], entry['value']))
        return urls
    else:
        raise ValueError("Unknown league for get_all_scoreboard_urls")

def get_season_start_end_datetimes_helper(url, driver):
    scoreboard = get_scoreboard_json(url, driver)
    return {'calendarStartDate': scoreboard['leagues'][0]['calendarStartDate'], 
            'calendarEndDate': scoreboard['leagues'][0]['calendarEndDate']}

''' Guess a random date in a leagues season and return its calendar start and end dates, only non football adheres to this format'''
def get_season_start_end_datetimes(league, season_year, driver):
    if league == "mlb":
        return get_season_start_end_datetimes_helper(get_date_scoreboard_url(league, str(season_year) + "0415"), driver)
    elif league == "nba":
        return get_season_start_end_datetimes_helper(get_date_scoreboard_url(league, str(season_year - 1) + "1101"), driver)
    elif league == "ncb" or league == "wcb":
        return get_season_start_end_datetimes_helper(get_date_scoreboard_url(league, str(season_year - 1) + "1130"), driver)
    elif league == "wnba":
        return get_season_start_end_datetimes_helper(get_date_scoreboard_url(league, str(season_year) + "0530"), driver)
    else:
        raise ValueError("League must be mlb, nba, ncb to get season start and end datetimes")

''' Return a calendar list, only football adheres to this format '''
def get_calendar_list(league, season_year, driver):
    if league == "nfl":
        return get_scoreboard_json(get_week_scoreboard_url(league, season_year, 2, 1), driver)['leagues'][0]['calendar']
    elif league == "ncf":
        return get_scoreboard_json(get_week_scoreboard_url(league, season_year, 2, 1), driver)['leagues'][0]['calendar']
    else:
        raise ValueError("League must be nfl,ncf to get calendar list")

''' Make an http get request to ESPN to get new scoreboard json '''
def get_new_scoreboard_json(url, driver):
    print(url)
    driver.get(url)
    driver.implicitly_wait(1)
    script_text = re.search(r'window\.espn\.scoreboardData\s*=.*<\/script>', driver.page_source)
    seconds = 1
    timeout = 15
    # if still none, wait up to timeout seconds to try to find scoreboardData
    while script_text is None:
        driver.implicitly_wait(1)
        script_text = re.search(r'window\.espn\.scoreboardData\s*=.*<\/script>', driver.page_source)
        seconds += 1
        if seconds > timeout:
            raise ValueError("Couldn't find scoreboard JSON data after {} seconds at {}".format(timeout, url))
    script_text = script_text.group(0)

    # split text based on first equal sign and remove trailing script tag and semicolon
    json_text = script_text.split('=',1)[1].rstrip('</script>').strip().rstrip(';').strip()
    # only care about first piece of json
    json_text = json_text.split("};")[0] + "}"
    return json.loads(json_text)

''' Retrieve an ESPN scoreboard JSON data, either from cache or make new request '''
def get_scoreboard_json(url, driver, cached_json_path=None, cache_json=False, use_cached_json=False):
    # add slash if necessary to cached_json_path
    if cached_json_path != None:
        if cached_json_path[-1] != "/":
            cached_json_path += "/"
        filename = cached_json_path + url.replace('/','-') + ".json"
    found_cached_json = False
    if use_cached_json:
        if os.path.isfile(filename):
            with open(filename) as json_data:
                data = json.load(json_data)
            found_cached_json = True
    if found_cached_json == False:
        data = get_new_scoreboard_json(url, driver)
        if cache_json:
            with open(filename, 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
    return data
