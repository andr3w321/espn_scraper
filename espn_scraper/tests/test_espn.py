from unittest import TestCase

import espn_scraper as espn
from selenium import webdriver

class TestEspn(TestCase):
    def test_get_leagues(self):
        assert(len(espn.get_leagues()) == 7)
    def test_get_num_nfl_teams(self):
        assert(len(espn.get_teams("nfl")) == 32)
    def test_get_num_mlb_teams(self):
        assert(len(espn.get_teams("mlb")) == 30)
    def test_get_num_nba_teams(self):
        assert(len(espn.get_teams("nba")) == 30)
    def test_get_num_ncf_teams(self):
        assert(len(espn.get_teams("ncb")) == 254)
    def test_get_num_ncf_teams(self):
        assert(len(espn.get_teams("ncb")) == 351)
    def test_get_num_ncw_teams(self):
        assert(len(espn.get_teams("ncw")) > 300)
    def test_get_num_wnba_teams(self):
        assert(len(espn.get_teams("wnba")) == 12)

    def test_nfl_scorebaord(self):
        data = espn.get_new_json("http://www.espn.com/nfl/scoreboard/_/year/2015/seasontype/2/week/1?xhr=1")
        assert(len(data['content']['sbData']['events']) == 16)
    def test_mlb_scorebaord(self):
        data = espn.get_json("http://www.espn.com/mlb/scoreboard/_/date/20160601?xhr=1", "scoreboards")
        assert(len(data['content']['sbData']['events'])== 15)
    def test_ncf_scorebaord(self):
        data = espn.get_json("http://www.espn.com/college-football/scoreboard/_/year/2016/seasontype/2/week/3?xhr=1", "scoreboards")
        assert(len(data['content']['sbData']['events']) == 21)
    def test_ncb_scorebaord(self):
        data = espn.get_json("http://www.espn.com/mens-college-basketball/scoreboard/_/group/50/date/20170211?xhr=1", "scoreboards")
        assert(len(data['content']['sbData']['events']) == 146)
    def test_wcb_scorebaord(self):
        data = espn.get_json("http://www.espn.com/womens-college-basketball/scoreboard/_/date/20170120?xhr=1", "scoreboards")
        assert(len(data['content']['sbData']['events']) == 3)
    def test_wnba_scorebaord(self):
        data = espn.get_json("http://www.espn.com/wnba/scoreboard/_/date/20160710?xhr=1", "scoreboards")
        # should redirect to different url
        assert(len(data['content']) == 5)

