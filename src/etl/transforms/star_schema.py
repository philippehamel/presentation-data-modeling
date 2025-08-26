from datetime import datetime
import pandas as pd

def create_star_schema(pitch_data: pd.DataFrame, player_data: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
    """
    Create star schema for MLB pitch data.

    Args:
        pitch_data: DataFrame containing pitch-by-pitch data.
        player_data: DataFrame containing player information.

    Returns:
        Tuple of DataFrames: (fact table, game dimension, player dimension)
    """
    # Create Game Dimension
    game_dim = pitch_data[['game_pk', 'game_date', 'home_team', 'away_team']].drop_duplicates()
    game_dim['game_key'] = range(1, len(game_dim) + 1)
    
    # Create Player Dimension
    player_dim = player_data[['mlb_id', 'full_name', 'position', 'bats', 'throws']].drop_duplicates()
    player_dim['player_key'] = range(1, len(player_dim) + 1)

    # Create Fact Table
    fact_table = pitch_data.copy()
    fact_table = fact_table.merge(game_dim[['game_pk', 'game_key']], on='game_pk', how='left')
    fact_table = fact_table.merge(player_dim[['mlb_id', 'player_key']], left_on='pitcher', right_on='mlb_id', how='left')
    fact_table = fact_table.merge(player_dim[['mlb_id', 'player_key']], left_on='batter', right_on='mlb_id', how='left', suffixes=('_pitcher', '_batter'))
    
    # Select relevant columns for the fact table
    fact_table = fact_table[['game_key', 'player_key_pitcher', 'player_key_batter', 'pitch_number', 'inning', 'pitch_type', 'release_speed', 'release_spin_rate', 'events']]
    
    return fact_table, game_dim, player_dim

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