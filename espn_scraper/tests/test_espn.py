from unittest import TestCase

import espn_scraper as espn

class TestEspn(TestCase):
    def test_leagues(self):
        assert(espn.get_leagues() == ["nfl","mlb","nba","ncf","ncb"])
