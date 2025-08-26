import pandas as pd
import requests
from io import StringIO


class StatcastClient:
    def __init__(self, start_date: str, end_date: str, teams: str = "TOR|COL"):
        self.start_date = start_date
        self.end_date = end_date
        self.teams = teams
        self.base_url = "https://baseballsavant.mlb.com/statcast_search/csv"

    def fetch_data(self):
        params = {
            "all": "true",
            "hfPT": "",
            "hfAB": "",
            "hfBBT": "",
            "hfPR": "",
            "hfZ": "",
            "stadium": "",
            "hfBBL": "",
            "hfNewZones": "",
            "hfGT": "R",  # Regular season
            "hfC": "",
            "hfSea": "2025",
            "hfSit": "",
            "player_type": "pitcher",
            "hfOuts": "",
            "opponent": "",
            "pitcher_throws": "",
            "batter_stands": "",
            "hfSA": "",
            "game_date_gt": self.start_date,
            "game_date_lt": self.end_date,
            "team": self.teams,
            "position": "",
            "hfRO": "",
            "home_road": "",
            "hfFlag": "",
            "metric_1": "",
            "hfInn": "",
            "min_pitches": "0",
            "min_results": "0",
            "group_by": "name",
            "sort_col": "pitches",
            "player_event_sort": "h_launch_speed",
            "sort_order": "desc",
            "min_abs": "0",
            "type": "details",
        }

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()

        return pd.read_csv(StringIO(response.text))
