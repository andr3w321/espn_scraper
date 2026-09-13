import datetime
from unittest import TestCase
from unittest.mock import patch

import espn_scraper as espn


SCOREBOARD = {
    "leagues": [{
        "calendarStartDate": "2024-09-24T07:00Z",
        "calendarEndDate": "2024-09-26T06:59Z",
    }],
    "events": [],
}


class TestSeasonDiscovery(TestCase):
    def test_v2_calendar_dates_keep_their_timezones(self):
        url = espn.get_date_scoreboard_url("nba", "20241101")
        with patch.object(espn, "get_new_json", return_value=SCOREBOARD):
            start, end = espn.get_season_start_end_datetimes_helper(url)
        self.assertEqual(start, datetime.datetime(2024, 9, 24, 7, tzinfo=datetime.timezone.utc))
        self.assertEqual(end, datetime.datetime(2024, 9, 26, 6, 59, tzinfo=datetime.timezone.utc))

    def assert_season_urls(self, league, sport, path, probe_date, suffixes):
        with patch.object(espn, "get_new_json", return_value=SCOREBOARD) as fetch:
            urls = espn.get_all_scoreboard_urls(league, 2025)
        base = "https://site.api.espn.com/apis/site/v2/sports/{}/{}/scoreboard?dates=".format(sport, path)
        fetch.assert_called_once_with(base + probe_date, espn.DEFAULT_HEADERS)
        self.assertEqual(urls, [
            base + date + suffix
            for date in ["20240924", "20240925"]
            for suffix in suffixes
        ])

    def test_nba_season_urls(self):
        self.assert_season_urls("nba", "basketball", "nba", "20241101", [""])

    def test_mlb_season_urls(self):
        self.assert_season_urls("mlb", "baseball", "mlb", "20250415", [""])

    def test_ncb_season_urls_preserve_groups(self):
        self.assert_season_urls("ncb", "basketball", "mens-college-basketball", "20241130", [
            "&groups=50&limit=1000", "&groups=55&limit=1000",
            "&groups=56&limit=1000", "&groups=100&limit=1000",
        ])

    def test_ncw_season_urls_preserve_groups(self):
        self.assert_season_urls("ncw", "basketball", "womens-college-basketball", "20241130", [
            "&groups=50&limit=1000", "&groups=55&limit=1000", "&groups=100&limit=1000",
        ])
