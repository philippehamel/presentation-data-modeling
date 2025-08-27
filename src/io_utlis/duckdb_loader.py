from duckdb import connect
import os


def load_csv_to_duckdb(db_path: str, csv_path: str, table_name: str):
    """Load CSV data into DuckDB."""
    conn = connect(db_path)
    conn.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM read_csv_auto('{csv_path}')"
    )
    conn.close()


def load_parquet_to_duckdb(db_path: str, parquet_path: str, table_name: str):
    """Load Parquet data into DuckDB."""
    conn = connect(db_path)
    conn.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM read_parquet('{parquet_path}')"
    )
    conn.close()


def main():
    """Main function to load data into DuckDB."""
    db_path = os.path.join("db", "duckdb", "mlb_data.duckdb")

    # Load Star Schema Parquet files
    load_parquet_to_duckdb(
        db_path,
        os.path.join("data", "processed", "star", "dim_game.parquet"),
        "star_dim_game",
    )
    load_parquet_to_duckdb(
        db_path,
        os.path.join("data", "processed", "star", "dim_player.parquet"),
        "star_dim_player",
    )
    load_parquet_to_duckdb(
        db_path,
        os.path.join("data", "processed", "star", "dim_count.parquet"),
        "star_dim_count",
    )
    load_parquet_to_duckdb(
        db_path,
        os.path.join("data", "processed", "star", "fact_pitch.parquet"),
        "star_fact_pitch",
    )

    # Load Snowflake Schema Parquet files
    load_parquet_to_duckdb(
        db_path,
        os.path.join("data", "processed", "snowflake", "dim_game.parquet"),
        "snowflake_dim_game",
    )
    load_parquet_to_duckdb(
        db_path,
        os.path.join("data", "processed", "snowflake", "dim_player.parquet"),
        "snowflake_dim_player",
    )
    load_parquet_to_duckdb(
        db_path,
        os.path.join("data", "processed", "snowflake", "dim_count.parquet"),
        "snowflake_dim_count",
    )
    load_parquet_to_duckdb(
        db_path,
        os.path.join("data", "processed", "snowflake", "dim_position.parquet"),
        "snowflake_dim_position",
    )
    load_parquet_to_duckdb(
        db_path,
        os.path.join("data", "processed", "snowflake", "dim_birth_location.parquet"),
        "snowflake_dim_birth_location",
    )
    load_parquet_to_duckdb(
        db_path,
        os.path.join("data", "processed", "snowflake", "fact_pitch.parquet"),
        "snowflake_fact_pitch",
    )

    # Load One Big Table Parquet file
    load_parquet_to_duckdb(
        db_path,
        os.path.join("data", "processed", "obt", "one_big_table.parquet"),
        "one_big_table",
    )


if __name__ == "__main__":
    main()
