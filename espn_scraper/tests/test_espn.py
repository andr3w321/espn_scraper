from unittest import TestCase

import espn_scraper as espn
from selenium import webdriver

class TestEspn(TestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS(service_args=['--load-images=no'])
    def tearDown(self):
        self.driver.quit()

    def test_get_leagues(self):
        assert(espn.get_leagues() == ["nfl","mlb","nba","ncf","ncb","wcb","wnba"])
    def test_get_num_nfl_teams(self):
        assert(len(espn.get_teams("nfl", self.driver)) == 32)
    def test_get_num_mlb_teams(self):
        assert(len(espn.get_teams("mlb", self.driver)) == 30)
    def test_get_num_nba_teams(self):
        assert(len(espn.get_teams("nba", self.driver)) == 30)
    def test_get_num_ncf_teams(self):
        assert(len(espn.get_teams("ncb", self.driver)) == 254)
    def test_get_num_ncf_teams(self):
        assert(len(espn.get_teams("ncb", self.driver)) == 351)
    def test_get_num_wcb_teams(self):
        assert(len(espn.get_teams("wcb", self.driver)) > 300)
    def test_get_num_wnba_teams(self):
        assert(len(espn.get_teams("wnba", self.driver)) == 12)

    def test_nfl_scorebaord(self):
        data = espn.get_scoreboard_json("http://www.espn.com/nfl/scoreboard/_/year/2015/seasontype/2/week/1", self.driver)
        assert(len(data['events']) == 16)
    def test_mlb_scorebaord(self):
        data = espn.get_scoreboard_json("http://www.espn.com/mlb/scoreboard/_/date/20160601", self.driver)
        assert(len(data['events'])== 15)
    def test_ncf_scorebaord(self):
        data = espn.get_scoreboard_json("http://www.espn.com/college-football/scoreboard/_/year/2016/seasontype/2/week/3", self.driver)
        assert(len(data['events']) == 21)
    def test_ncb_scorebaord(self):
        data = espn.get_scoreboard_json("http://www.espn.com/mens-college-basketball/scoreboard/_/group/50/date/20170211", self.driver)
        assert(len(data['events']) == 146)
    def test_wcb_scorebaord(self):
        data = espn.get_scoreboard_json("http://www.espn.com/womens-college-basketball/scoreboard/_/date/20170120", self.driver)
        assert(len(data['events']) == 3)
    def test_wnba_scorebaord(self):
        data = espn.get_scoreboard_json("http://www.espn.com/wnba/scoreboard/_/date/20160710", self.driver)
        # should redirect to different url
        assert(len(data['content']) == 5)

