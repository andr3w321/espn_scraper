import espn_scraper as espn
from selenium import webdriver
import json

''' Pretty print json '''
def ppjson(data):
    print(json.dumps(data, indent=2, sort_keys=True))

driver = webdriver.PhantomJS(service_args=['--load-images=no'])

print(espn.get_leagues())
print(espn.get_teams("nfl", driver))

scoreboard_urls = espn.get_all_scoreboard_urls("nfl", 2016, driver)
for scoreboard_url in scoreboard_urls:
    data = espn.get_scoreboard_json(scoreboard_url, driver, cached_json_path="cached_json", cache_json=True, use_cached_json=True)
    for event in data['events']:
        if event['season']['type'] == 3:
            print(event['season']['type'],
                  event['season']['year'],
                  event['competitions'][0]['competitors'][0]['team']['abbreviation'],
                  event['competitions'][0]['competitors'][0]['score'],
                  event['competitions'][0]['competitors'][1]['team']['abbreviation'],
                  event['competitions'][0]['competitors'][1]['score'])

driver.quit()
