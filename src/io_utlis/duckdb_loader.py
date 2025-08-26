from duckdb import connect
import os

def load_csv_to_duckdb(db_path: str, csv_path: str, table_name: str):
    """Load CSV data into DuckDB."""
    conn = connect(db_path)
    conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM read_csv_auto('{csv_path}')")
    conn.close()

def load_parquet_to_duckdb(db_path: str, parquet_path: str, table_name: str):
    """Load Parquet data into DuckDB."""
    conn = connect(db_path)
    conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM read_parquet('{parquet_path}')")
    conn.close()

def main():
    """Main function to load data into DuckDB."""
    db_path = os.path.join('db', 'duckdb', 'mlb_data.duckdb')
    
    # Load CSV files
    load_csv_to_duckdb(db_path, os.path.join('data', 'processed', 'star', 'dim_game.csv'), 'dim_game')
    load_csv_to_duckdb(db_path, os.path.join('data', 'processed', 'star', 'dim_player.csv'), 'dim_player')
    load_csv_to_duckdb(db_path, os.path.join('data', 'processed', 'star', 'dim_count.csv'), 'dim_count')
    load_csv_to_duckdb(db_path, os.path.join('data', 'processed', 'star', 'fact_pitches.csv'), 'fact_pitches')
    
    # Load Parquet files
    load_parquet_to_duckdb(db_path, os.path.join('data', 'processed', 'snowflake', 'dim_game_snowflake.parquet'), 'dim_game_snowflake')
    load_parquet_to_duckdb(db_path, os.path.join('data', 'processed', 'snowflake', 'dim_player_snowflake.parquet'), 'dim_player_snowflake')
    load_parquet_to_duckdb(db_path, os.path.join('data', 'processed', 'snowflake', 'dim_stadium.parquet'), 'dim_stadium')
    load_parquet_to_duckdb(db_path, os.path.join('data', 'processed', 'snowflake', 'dim_team.parquet'), 'dim_team')
    load_parquet_to_duckdb(db_path, os.path.join('data', 'processed', 'snowflake', 'dim_position.parquet'), 'dim_position')
    load_parquet_to_duckdb(db_path, os.path.join('data', 'processed', 'snowflake', 'dim_birth_location.parquet'), 'dim_birth_location')
    
    # Load One Big Table
    load_csv_to_duckdb(db_path, os.path.join('data', 'processed', 'obt', 'one_big_table.csv'), 'one_big_table')

if __name__ == "__main__":
    main()