from datetime import datetime
import os
import sys
import pandas as pd
import numpy as np
import requests
import logging
from typing import Dict, List
from io import StringIO
from pathlib import Path

# Add parent directory to path for imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MLBDataPipeline:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.create_directories()

        # MLB API base URLs
        self.mlb_api_base = "https://statsapi.mlb.com/api/v1"
        self.savant_base = "https://baseballsavant.mlb.com/statcast_search/csv"

        # Team mappings
        self.team_mapping = {
            "TOR": {"id": 142, "name": "Toronto Blue Jays"},
            "COL": {"id": 115, "name": "Colorado Rockies"},
        }

    def create_directories(self):
        """Create necessary directories for data storage."""
        os.makedirs(f"{self.data_dir}/raw/statcast", exist_ok=True)
        os.makedirs(f"{self.data_dir}/raw/mlb", exist_ok=True)
        os.makedirs(f"{self.data_dir}/processed/star", exist_ok=True)
        os.makedirs(f"{self.data_dir}/processed/snowflake", exist_ok=True)
        os.makedirs(f"{self.data_dir}/processed/obt", exist_ok=True)
        logger.info(f"Created data directories under: {self.data_dir}")

    def download_statcast_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Download Statcast pitch-by-pitch data from Baseball Savant.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            DataFrame with pitch-by-pitch data
        """
        logger.info(f"Downloading Statcast data from {start_date} to {end_date}")

        # Baseball Savant CSV export URL
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
            "hfGT": "R",
            "hfC": "",
            "hfSea": "2025",
            "hfSit": "",
            "player_type": "pitcher",
            "hfOuts": "",
            "opponent": "",
            "pitcher_throws": "",
            "batter_stands": "",
            "hfSA": "",
            "game_date_gt": start_date,
            "game_date_lt": end_date,
            "team": "TOR|COL",
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

        try:
            response = requests.get(self.savant_base, params=params, timeout=30)
            response.raise_for_status()

            # Use StringIO from io module instead of pandas.compat
            df = pd.read_csv(StringIO(response.text))

            # Save raw data
            raw_file = f"{self.data_dir}/raw/statcast/statcast_data_{start_date}_{end_date}.csv"
            df.to_csv(raw_file, index=False)
            logger.info(f"Saved raw Statcast data to {raw_file}")

            return df

        except Exception as e:
            logger.error(f"Error downloading Statcast data: {e}")
            # Return sample data if API fails
            return self.create_sample_data()

    def create_sample_data(self) -> pd.DataFrame:
        """Create sample pitch data for demonstration."""
        logger.info("Creating sample pitch data for demonstration")
        np.random.seed(42)

        sample_data = []
        game_pks = [776854, 776855, 776856]  # Sample game IDs
        dates = ["2025-08-04", "2025-08-05", "2025-08-06"]

        for i, (game_pk, date) in enumerate(zip(game_pks, dates)):
            for pitch_num in range(1, 101):  # 100 pitches per game
                sample_data.append(
                    {
                        "game_pk": game_pk,
                        "game_date": date,
                        "home_team": "COL" if i % 2 == 0 else "TOR",
                        "away_team": "TOR" if i % 2 == 0 else "COL",
                        "inning": np.random.randint(1, 10),
                        "pitcher": np.random.randint(400000, 700000),
                        "batter": np.random.randint(400000, 700000),
                        "balls": np.random.randint(0, 4),
                        "strikes": np.random.randint(0, 3),
                        "pitch_type": np.random.choice(["FF", "SL", "CH", "CU", "SI"]),
                        "release_speed": np.random.normal(92, 5),
                        "description": np.random.choice(
                            ["ball", "called_strike", "swinging_strike", "foul"]
                        ),
                    }
                )

        return pd.DataFrame(sample_data)

    def get_player_data(self, player_ids: List[int]) -> pd.DataFrame:
        """
        Fetch player dimension data from MLB API.

        Args:
            player_ids: List of MLB player IDs

        Returns:
            DataFrame with player information
        """
        # Import here to avoid circular imports
        from etl.players_client import PlayersClient

        client = PlayersClient()
        return client.fetch_player_data(player_ids)

    def create_game_dimension(self, pitch_data: pd.DataFrame) -> pd.DataFrame:
        """Create game dimension table from pitch data."""
        logger.info("Creating game dimension table")

        games = (
            pitch_data.groupby(["game_pk", "game_date", "home_team", "away_team"])
            .agg({"inning": "max", "pitcher": "count"})  # Count of pitches
            .reset_index()
        )

        games["game_key"] = range(1, len(games) + 1)
        games["season"] = 2025
        games["game_type"] = "R"  # Regular season
        games["day_of_week"] = pd.to_datetime(games["game_date"]).dt.day_name()
        games["stadium"] = games["home_team"].map(
            {"TOR": "Rogers Centre", "COL": "Coors Field"}
        )
        games["weather_temp"] = 72  # Default temperature
        games["weather_condition"] = "Clear"
        games["total_pitches"] = games["pitcher"]  # Rename the count column

        games = games.drop("pitcher", axis=1)

        return games[
            [
                "game_key",
                "game_pk",
                "game_date",
                "season",
                "game_type",
                "home_team",
                "away_team",
                "stadium",
                "day_of_week",
                "weather_temp",
                "weather_condition",
                "total_pitches",
            ]
        ]

    def create_count_dimension(self) -> pd.DataFrame:
        """Create count dimension table with all possible ball/strike combinations."""
        logger.info("Creating count dimension table")

        counts = []
        count_key = 1

        for balls in range(4):  # 0-3 balls
            for strikes in range(3):  # 0-2 strikes
                counts.append(
                    {
                        "count_key": count_key,
                        "balls": balls,
                        "strikes": strikes,
                        "count_display": f"{balls}-{strikes}",
                        "count_category": self.categorize_count(balls, strikes),
                    }
                )
                count_key += 1

        return pd.DataFrame(counts)

    def categorize_count(self, balls: int, strikes: int) -> str:
        """Categorize the count as pitcher's count, hitter's count, or neutral."""
        if strikes > balls:
            return "Pitcher's Count"
        elif balls > strikes:
            return "Hitter's Count"
        else:
            return "Neutral Count"

    def create_snowflake_schema(
        self,
        pitch_data: pd.DataFrame,
        player_dim: pd.DataFrame,
        game_dim: pd.DataFrame,
        count_dim: pd.DataFrame,
    ):
        """Create and save snowflake schema (normalized)."""
        from etl.transforms.snowflake_schema import create_snowflake_schema

        snowflake_tables = create_snowflake_schema(pitch_data, player_dim)

        # Save each table
        for table_name, table_df in snowflake_tables.items():
            table_df.to_csv(
                f"{self.data_dir}/processed/snowflake/{table_name}.csv", index=False
            )
            table_df.to_parquet(
                f"{self.data_dir}/processed/snowflake/{table_name}.parquet", index=False
            )

        logger.info("Snowflake schema tables saved")

    def create_one_big_table_schema(
        self,
        pitch_data: pd.DataFrame,
        player_dim: pd.DataFrame,
        game_dim: pd.DataFrame,
        count_dim: pd.DataFrame,
    ):
        """Create and save one big table (denormalized)."""
        from etl.transforms.one_big_table import create_one_big_table

        big_table = create_one_big_table(pitch_data, game_dim, player_dim, count_dim)

        # Save the big table
        big_table.to_csv(
            f"{self.data_dir}/processed/obt/one_big_table.csv", index=False
        )
        big_table.to_parquet(
            f"{self.data_dir}/processed/obt/one_big_table.parquet", index=False
        )

        logger.info("One big table saved")

    def run_pipeline(self):
        """Run the complete data pipeline."""
        logger.info("Starting MLB data pipeline")

        # Download pitch data
        pitch_data = self.download_statcast_data("2025-08-04", "2025-08-06")

        # Create dimensions
        game_dim = self.create_game_dimension(pitch_data)
        count_dim = self.create_count_dimension()

        # Get unique player IDs and fetch player data
        pitcher_ids = pitch_data["pitcher"].dropna().unique().tolist()
        batter_ids = pitch_data["batter"].dropna().unique().tolist()
        all_player_ids = list(set(pitcher_ids + batter_ids))

        # Get all players (not limited to 10)
        player_dim = self.get_player_data(all_player_ids)

        # Save star schema data
        game_dim.to_csv(f"{self.data_dir}/processed/star/dim_game.csv", index=False)
        count_dim.to_csv(f"{self.data_dir}/processed/star/dim_count.csv", index=False)
        player_dim.to_csv(f"{self.data_dir}/processed/star/dim_player.csv", index=False)
        pitch_data.to_csv(f"{self.data_dir}/processed/star/fact_pitch.csv", index=False)

        # Also save as parquet
        game_dim.to_parquet(
            f"{self.data_dir}/processed/star/dim_game.parquet", index=False
        )
        count_dim.to_parquet(
            f"{self.data_dir}/processed/star/dim_count.parquet", index=False
        )
        player_dim.to_parquet(
            f"{self.data_dir}/processed/star/dim_player.parquet", index=False
        )
        pitch_data.to_parquet(
            f"{self.data_dir}/processed/star/fact_pitch.parquet", index=False
        )

        # Create and save snowflake schema
        self.create_snowflake_schema(pitch_data, player_dim, game_dim, count_dim)

        # Create and save one big table
        self.create_one_big_table_schema(pitch_data, player_dim, game_dim, count_dim)

        logger.info("Pipeline completed successfully")


def main():
    """Main execution function."""
    pipeline = MLBDataPipeline()
    pipeline.run_pipeline()


if __name__ == "__main__":
    main()
