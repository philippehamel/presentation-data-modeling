-- ==============================================
-- Load Parquet files into DuckDB (Recommended)
-- ==============================================

-- Star Schema Tables (using Parquet for better performance)
CREATE OR REPLACE TABLE star_dim_game AS SELECT * FROM read_parquet('data/processed/star/dim_game.parquet');
CREATE OR REPLACE TABLE star_dim_player AS SELECT * FROM read_parquet('data/processed/star/dim_player.parquet');
CREATE OR REPLACE TABLE star_dim_count AS SELECT * FROM read_parquet('data/processed/star/dim_count.parquet');
CREATE OR REPLACE TABLE star_fact_pitch AS SELECT * FROM read_parquet('data/processed/star/fact_pitch.parquet');

-- Snowflake Schema Tables (using Parquet for better performance)
CREATE OR REPLACE TABLE snowflake_dim_game AS SELECT * FROM read_parquet('data/processed/snowflake/dim_game.parquet');
CREATE OR REPLACE TABLE snowflake_dim_player AS SELECT * FROM read_parquet('data/processed/snowflake/dim_player.parquet');
CREATE OR REPLACE TABLE snowflake_dim_position AS SELECT * FROM read_parquet('data/processed/snowflake/dim_position.parquet');
CREATE OR REPLACE TABLE snowflake_dim_birth_location AS SELECT * FROM read_parquet('data/processed/snowflake/dim_birth_location.parquet');
CREATE OR REPLACE TABLE snowflake_dim_count AS SELECT * FROM read_parquet('data/processed/snowflake/dim_count.parquet');
CREATE OR REPLACE TABLE snowflake_fact_pitches AS SELECT * FROM read_parquet('data/processed/snowflake/fact_pitches.parquet');

-- One Big Table (using Parquet for better performance)
CREATE OR REPLACE TABLE one_big_table AS SELECT * FROM read_parquet('data/processed/obt/one_big_table.parquet');