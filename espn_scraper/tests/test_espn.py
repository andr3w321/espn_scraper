from unittest import TestCase
import espn_scraper as espn

def boxscore_helper(self, league, espn_id):
    data = espn.get_url(espn.get_game_url("boxscore", league, espn_id))
    self.assertEqual(data['gameId'], espn_id)

class TestEspn(TestCase):
    # leagues
    def test_get_leagues(self):
        self.assertEqual(len(espn.get_leagues()), 8)
    # teams
    def test_get_num_nfl_teams(self):
        self.assertEqual(len(espn.get_teams("nfl")), 32)
    def test_get_num_mlb_teams(self):
        self.assertEqual(len(espn.get_teams("mlb")), 30)
    def test_get_num_nba_teams(self):
        self.assertEqual(len(espn.get_teams("nba")), 30)
    def test_get_num_ncf_teams(self):
        self.assertEqual(len(espn.get_teams("ncb")), 254)
    def test_get_num_ncf_teams(self):
        self.assertEqual(len(espn.get_teams("ncb")), 351)
    def test_get_num_ncw_teams(self):
        assert(len(espn.get_teams("ncw")) > 300)
    def test_get_num_wnba_teams(self):
        self.assertEqual(len(espn.get_teams("wnba")), 12)
    def test_get_num_nhl_teams(self):
        self.assertEqual(len(espn.get_teams("nhl")), 30)

    # scoreboards
    def test_nfl_scoreboard(self):
        url = espn.get_week_scoreboard_url("nfl", 2015, 2, 1)
        data = espn.get_url(url)
        self.assertEqual(len(data['content']['sbData']['events']), 16)
    def test_mlb_scoreboard(self):
        url = espn.get_date_scoreboard_url("mlb", "20160601")
        data = espn.get_url(url)
        self.assertEqual(len(data['content']['sbData']['events']), 15)
    def test_ncf_scoreboard(self):
        url = espn.get_week_scoreboard_url("ncf", 2016, 2, 3)
        data = espn.get_url(url)
        self.assertEqual(len(data['content']['sbData']['events']), 21)
    def test_ncb_scoreboard(self):
        url = espn.get_date_scoreboard_url("ncb", "20170211", 50)
        data = espn.get_url(url)
        self.assertEqual(len(data['content']['sbData']['events']), 146)
    def test_ncw_scoreboard(self):
        url = espn.get_date_scoreboard_url("ncw", "20170120")
        data = espn.get_url(url)
        self.assertEqual(len(data['content']['sbData']['events']), 3)
    def test_wnba_scoreboard(self):
        url = espn.get_date_scoreboard_url("wnba", "20160710")
        data = espn.get_url(url)
        # should redirect to different url
        self.assertEqual(len(data['content']), 5)
    def test_nhl_scoreboard(self):
        url = espn.get_date_scoreboard_url("nhl", "20170328")
        data = espn.get_url(url)
        # should redirect to different url
        self.assertEqual(len(data['content']), 11)

    # scoreboards for a year
    def test_get_all_2016_nfl_scoreboard_urls(self):
        scoreboards = scoreboards = espn.get_all_scoreboard_urls("nfl", 2016)
        self.assertEqual(len(scoreboards), 27)

    # boxscores
    def test_nfl_boxscore(self):
        boxscore_helper(self, "nfl", 400874484)
    def test_nba_boxscore(self):
        boxscore_helper(self, "nba", 400900498)
    def test_mlb_boxscore(self):
        data = espn.get_url(espn.get_game_url("boxscore", "mlb", 370328119))
        away_score = int(data.select('.team-info span')[0].text.strip())
        home_score = int(data.select('.team-info span')[1].text.strip())
        self.assertEqual(away_score, 1)
        self.assertEqual(home_score, 3)
    def test_ncb_boxscore(self):
        boxscore_helper(self, "ncb", 400947330)
    def test_ncf_boxscore(self):
        boxscore_helper(self, "ncf", 400868977)
    def test_ncw_boxscore(self):
        boxscore_helper(self, "ncw", 400947271)
    def test_wnba_boxscore(self):
        data = espn.get_url(espn.get_game_url("boxscore", "wnba", 400910431))
        away_score = int(data.select('.team-info span')[0].text.strip())
        home_score = int(data.select('.team-info span')[1].text.strip())
        self.assertEqual(away_score, 85)
        self.assertEqual(home_score, 94)
