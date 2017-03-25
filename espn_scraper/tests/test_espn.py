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
        assert(len(espn.get_teams("wcb", self.driver)) == 349)
    def test_get_num_wnba_teams(self):
        assert(len(espn.get_teams("wnba", self.driver)) == 12)

