import pandas as pd
import requests
import logging
import json
import os
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class PlayersClient:
    def __init__(
        self, api_base: str = "https://statsapi.mlb.com/api/v1", save_raw: bool = True
    ):
        self.api_base = api_base
        self.save_raw = save_raw

        # Create raw data directory if saving raw data
        if self.save_raw:
            os.makedirs("data/raw/mlb", exist_ok=True)

    def fetch_player_data(self, player_ids: List[int]) -> pd.DataFrame:
        """
        Fetch player data from the MLB API for given player IDs.

        Args:
            player_ids: List of player IDs to fetch data for.

        Returns:
            DataFrame containing player information.
        """
        logger.info(f"Fetching player data for {len(player_ids)} players")
        players = []
        raw_responses = []

        for player_id in player_ids:
            try:
                url = f"{self.api_base}/people/{player_id}"
                response = requests.get(url)
                response.raise_for_status()

                data = response.json()

                # Save raw response if enabled
                if self.save_raw:
                    raw_responses.append(
                        {
                            "player_id": player_id,
                            "url": url,
                            "timestamp": datetime.now().isoformat(),
                            "response": data,
                        }
                    )

                if "people" in data and len(data["people"]) > 0:
                    player_info = self.extract_player_info(data["people"][0])
                    players.append(player_info)

            except Exception as e:
                logger.error(f"Error fetching data for player {player_id}: {e}")
                continue

        # Save all raw responses to a single file
        if self.save_raw and raw_responses:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            raw_file = f"data/raw/mlb/player_api_responses_{timestamp}.json"
            with open(raw_file, "w") as f:
                json.dump(raw_responses, f, indent=2)
            logger.info(
                f"Saved {len(raw_responses)} raw MLB API responses to {raw_file}"
            )

        return pd.DataFrame(players)

    def extract_player_info(self, player_data: Dict) -> Dict:
        """Extract relevant player information from API response."""
        return {
            "player_id": player_data.get("id"),
            "full_name": player_data.get("fullName"),
            "first_name": player_data.get("firstName"),
            "last_name": player_data.get("lastName"),
            "primary_number": player_data.get("primaryNumber"),
            "birth_date": player_data.get("birthDate"),
            "birth_city": player_data.get("birthCity"),
            "birth_state_province": player_data.get("birthStateProvince"),
            "birth_country": player_data.get("birthCountry"),
            "height": player_data.get("height"),
            "weight": player_data.get("weight"),
            "active": player_data.get("active"),
            "primary_position": player_data.get("primaryPosition", {}).get("name"),
            "bat_side": player_data.get("batSide", {}).get("description"),
            "pitch_hand": player_data.get("pitchHand", {}).get("description"),
            "mlb_debut_date": player_data.get("mlbDebutDate"),
            "current_team_id": player_data.get("currentTeam", {}).get("id"),
            "current_team_name": player_data.get("currentTeam", {}).get("name"),
            "effective_date": datetime.now().isoformat(),
            "expiration_date": None,
            "is_current": True,
        }
