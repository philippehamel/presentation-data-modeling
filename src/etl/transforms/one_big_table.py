from typing import Dict
import pandas as pd


def create_one_big_table(
    pitch_data: pd.DataFrame,
    game_dim: pd.DataFrame,
    player_dim: pd.DataFrame,
    count_dim: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create a fully denormalized "one big table" with all data.

    Args:
        pitch_data: Raw pitch data
        game_dim: Game dimension
        player_dim: Player dimension
        count_dim: Count dimension

    Returns:
        Completely denormalized DataFrame
    """
    # Start with pitch data
    big_table = pitch_data.copy()

    # Add game information
    big_table = big_table.merge(
        game_dim.drop("game_key", axis=1),
        on="game_pk",
        how="left",
        suffixes=("", "_game"),
    )

    # Add pitcher information
    pitcher_info = player_dim[player_dim["is_current"] == True].copy()
    pitcher_cols = [
        "player_id",
        "full_name",
        "first_name",
        "last_name",
        "birth_date",
        "birth_city",
        "birth_country",
        "height",
        "weight",
        "bat_side",
        "pitch_hand",
        "primary_position",
        "mlb_debut_date",
    ]
    pitcher_rename = {
        col: f"pitcher_{col}" for col in pitcher_cols if col != "player_id"
    }
    pitcher_rename["player_id"] = "pitcher"

    big_table = big_table.merge(
        pitcher_info[pitcher_cols].rename(columns=pitcher_rename),
        on="pitcher",
        how="left",
    )

    # Add batter information
    batter_info = player_dim[player_dim["is_current"] == True].copy()
    batter_rename = {col: f"batter_{col}" for col in pitcher_cols if col != "player_id"}
    batter_rename["player_id"] = "batter"

    big_table = big_table.merge(
        batter_info[pitcher_cols].rename(columns=batter_rename), on="batter", how="left"
    )

    # Add count information
    big_table = big_table.merge(
        count_dim.drop("count_key", axis=1), on=["balls", "strikes"], how="left"
    )

    # Add derived fields
    big_table["velocity_tier"] = big_table["release_speed"].apply(categorize_velocity)
    big_table["is_strike"] = big_table["type"] == "S"
    big_table["is_ball"] = big_table["type"] == "B"
    big_table["is_in_play"] = big_table["type"] == "X"
    big_table["is_swing_and_miss"] = big_table["description"] == "swinging_strike"
    big_table["is_hit"] = big_table["events"].isin(
        ["single", "double", "triple", "home_run"]
    )
    big_table["is_home_run"] = big_table["events"] == "home_run"
    big_table["is_strikeout"] = big_table["events"] == "strikeout"
    big_table["is_walk"] = big_table["events"] == "walk"

    return big_table


def categorize_velocity(velocity: float) -> str:
    """Categorize pitch velocity into tiers."""
    if pd.isna(velocity):
        return "Unknown"
    elif velocity < 80:
        return "Slow"
    elif velocity < 90:
        return "Medium"
    elif velocity < 95:
        return "Fast"
    else:
        return "Very Fast"
