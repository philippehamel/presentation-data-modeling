from typing import Dict
import pandas as pd


def create_snowflake_schema(
    pitch_data: pd.DataFrame, player_data: pd.DataFrame
) -> Dict[str, pd.DataFrame]:
    """
    Create normalized dimensions for snowflake schema (3NF).

    Args:
        pitch_data: Raw pitch data DataFrame.
        player_data: Player data DataFrame.

    Returns:
        Dictionary of normalized dimension tables and fact table.
    """
    # Create game dimension
    game_dim = (
        pitch_data.groupby(["game_pk", "game_date", "home_team", "away_team"])
        .agg({"inning": "max", "pitch_number": "count"})
        .reset_index()
    )

    game_dim["game_key"] = range(1, len(game_dim) + 1)
    game_dim["season"] = 2025
    game_dim["game_type"] = "R"  # Regular season
    game_dim["day_of_week"] = pd.to_datetime(game_dim["game_date"]).dt.day_name()
    game_dim["stadium"] = game_dim["home_team"].map(
        {"TOR": "Rogers Centre", "COL": "Coors Field"}
    )

    # Create player dimension
    player_dim = player_data[
        [
            "player_id",
            "full_name",
            "first_name",
            "last_name",
            "birth_city",
            "birth_country",
            "primary_position",
        ]
    ].drop_duplicates()
    player_dim["player_key"] = range(1, len(player_dim) + 1)

    # Create position dimension
    position_dim = player_dim[["primary_position"]].drop_duplicates()
    position_dim = position_dim[position_dim["primary_position"].notna()].copy()
    position_dim["position_key"] = range(1, len(position_dim) + 1)

    # Create birth location dimension
    birth_location_dim = player_dim[["birth_city", "birth_country"]].drop_duplicates()
    birth_location_dim = birth_location_dim.dropna().copy()
    birth_location_dim["location_key"] = range(1, len(birth_location_dim) + 1)

    # Add foreign keys to player dimension - remove birth location details after creating FKs
    player_dim = player_dim.merge(
        position_dim[["primary_position", "position_key"]],
        on="primary_position",
        how="left",
    )
    player_dim = player_dim.merge(
        birth_location_dim[["birth_city", "birth_country", "location_key"]],
        on=["birth_city", "birth_country"],
        how="left",
    )

    # For proper snowflake normalization, remove birth location details from player dimension
    # Keep only the foreign key reference
    player_dim = player_dim.drop(columns=["birth_city", "birth_country"])

    # Create count dimension - using same structure as star schema for consistency
    count_dim = []
    count_key = 1

    for balls in range(4):
        for strikes in range(3):
            count_display = f"{balls}-{strikes}"

            # Categorize count as in star schema
            if balls > strikes:
                count_category = "Hitter's Count"
            elif strikes > balls:
                count_category = "Pitcher's Count"
            else:
                count_category = "Neutral Count"

            count_dim.append(
                {
                    "count_key": count_key,
                    "balls": balls,
                    "strikes": strikes,
                    "count_display": count_display,
                    "count_category": count_category,
                }
            )
            count_key += 1

    count_dim = pd.DataFrame(count_dim)

    # Create fact table
    fact = pitch_data.copy()
    fact = fact.merge(game_dim[["game_pk", "game_key"]], on="game_pk", how="left")
    fact = fact.merge(
        player_dim[["player_id", "player_key"]],
        left_on="pitcher",
        right_on="player_id",
        how="left",
    )
    fact = fact.merge(
        player_dim[["player_id", "player_key"]],
        left_on="batter",
        right_on="player_id",
        how="left",
        suffixes=("_pitcher", "_batter"),
    )
    fact = fact.merge(
        count_dim[["balls", "strikes", "count_key"]],
        on=["balls", "strikes"],
        how="left",
    )

    return {
        "dim_game": game_dim,
        "dim_player": player_dim,
        "dim_position": position_dim,
        "dim_birth_location": birth_location_dim,
        "dim_count": count_dim,
        "fact_pitches": fact,
    }
