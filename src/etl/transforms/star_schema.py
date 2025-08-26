from datetime import datetime
import pandas as pd

def create_star_schema(
    pitch_data: pd.DataFrame,
    game_dim: pd.DataFrame,
    player_dim: pd.DataFrame,
    count_dim: pd.DataFrame,
) -> dict:
    """
    Create star schema for MLB pitch data with proper foreign key relationships.

    Args:
        pitch_data: DataFrame containing pitch-by-pitch data.
        game_dim: DataFrame containing game dimension data with game_key.
        player_dim: DataFrame containing player dimension data with player_id.
        count_dim: DataFrame containing count dimension data with count_key.

    Returns:
        Dictionary of DataFrames: fact_pitch with proper foreign keys
    """
    # Create fact table with foreign keys
    fact = pitch_data.copy()

    # Add game_key from game dimension
    fact = fact.merge(game_dim[["game_pk", "game_key"]], on="game_pk", how="left")

    # Add pitcher foreign key (player_id is the primary key)
    fact = fact.merge(
        player_dim[["player_id"]], 
        left_on="pitcher", 
        right_on="player_id", 
        how="left",
        suffixes=("", "_pitcher_fk")
    )
    
    # Add batter foreign key  
    fact = fact.merge(
        player_dim[["player_id"]], 
        left_on="batter", 
        right_on="player_id", 
        how="left", 
        suffixes=("", "_batter_fk")
    )

    # Add count foreign key
    fact = fact.merge(
        count_dim[["balls", "strikes", "count_key"]], 
        on=["balls", "strikes"], 
        how="left"
    )

    return {
        "fact_pitch": fact
    }

def save_star_schema_to_csv(fact_table: pd.DataFrame, game_dim: pd.DataFrame, player_dim: pd.DataFrame, output_dir: str):
    """
    Save star schema tables to CSV files.

    Args:
        fact_table: Fact table DataFrame.
        game_dim: Game dimension DataFrame.
        player_dim: Player dimension DataFrame.
        output_dir: Directory to save CSV files.
    """
    fact_table.to_csv(f"{output_dir}/fact_table.csv", index=False)
    game_dim.to_csv(f"{output_dir}/game_dimension.csv", index=False)
    player_dim.to_csv(f"{output_dir}/player_dimension.csv", index=False)

def save_star_schema_to_parquet(fact_table: pd.DataFrame, game_dim: pd.DataFrame, player_dim: pd.DataFrame, output_dir: str):
    """
    Save star schema tables to Parquet files.

    Args:
        fact_table: Fact table DataFrame.
        game_dim: Game dimension DataFrame.
        player_dim: Player dimension DataFrame.
        output_dir: Directory to save Parquet files.
    """
    fact_table.to_parquet(f"{output_dir}/fact_table.parquet", index=False)
    game_dim.to_parquet(f"{output_dir}/game_dimension.parquet", index=False)
    player_dim.to_parquet(f"{output_dir}/player_dimension.parquet", index=False)
