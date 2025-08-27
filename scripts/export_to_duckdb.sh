#!/bin/bash

# This script exports the processed data to DuckDB for querying.

echo "==================================="
echo "MLB Data Export to DuckDB"
echo "==================================="

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Define DuckDB database file path
DUCKDB_DB_PATH="db/duckdb/mlb_data.duckdb"

# Create directory if it doesn't exist
mkdir -p "$(dirname "$DUCKDB_DB_PATH")"

echo "Creating DuckDB database and loading data..."

# Create DuckDB database and load all schema tables
echo "Creating DuckDB database at $DUCKDB_DB_PATH"
duckdb "$DUCKDB_DB_PATH" <<EOF
-- ======================
-- STAR SCHEMA TABLES (PARQUET)
-- ======================
CREATE OR REPLACE TABLE star_dim_game AS SELECT * FROM read_parquet('data/processed/star/dim_game.parquet');
CREATE OR REPLACE TABLE star_dim_player AS SELECT * FROM read_parquet('data/processed/star/dim_player.parquet');
CREATE OR REPLACE TABLE star_dim_count AS SELECT * FROM read_parquet('data/processed/star/dim_count.parquet');
CREATE OR REPLACE TABLE star_fact_pitch AS SELECT * FROM read_parquet('data/processed/star/fact_pitch.parquet');

-- ======================
-- SNOWFLAKE SCHEMA TABLES (PARQUET)
-- ======================
CREATE OR REPLACE TABLE snowflake_dim_game AS SELECT * FROM read_parquet('data/processed/snowflake/dim_game.parquet');
CREATE OR REPLACE TABLE snowflake_dim_player AS SELECT * FROM read_parquet('data/processed/snowflake/dim_player.parquet');
CREATE OR REPLACE TABLE snowflake_dim_position AS SELECT * FROM read_parquet('data/processed/snowflake/dim_position.parquet');
CREATE OR REPLACE TABLE snowflake_dim_birth_location AS SELECT * FROM read_parquet('data/processed/snowflake/dim_birth_location.parquet');
CREATE OR REPLACE TABLE snowflake_dim_count AS SELECT * FROM read_parquet('data/processed/snowflake/dim_count.parquet');
CREATE OR REPLACE TABLE snowflake_fact_pitch AS SELECT * FROM read_parquet('data/processed/snowflake/fact_pitch.parquet');

-- ======================
-- ONE BIG TABLE (PARQUET)
-- ======================
CREATE OR REPLACE TABLE one_big_table AS SELECT * FROM read_parquet('data/processed/obt/one_big_table.parquet');

-- Show all tables
.tables

-- Show table summaries
SELECT 'STAR SCHEMA' as schema_type, 'star_dim_game' as table_name, COUNT(*) as row_count FROM star_dim_game
UNION ALL
SELECT 'STAR SCHEMA', 'star_dim_player', COUNT(*) FROM star_dim_player
UNION ALL
SELECT 'STAR SCHEMA', 'star_dim_count', COUNT(*) FROM star_dim_count
UNION ALL
SELECT 'STAR SCHEMA', 'star_fact_pitch', COUNT(*) FROM star_fact_pitch
UNION ALL
SELECT 'SNOWFLAKE SCHEMA', 'snowflake_dim_game', COUNT(*) FROM snowflake_dim_game
UNION ALL
SELECT 'SNOWFLAKE SCHEMA', 'snowflake_dim_player', COUNT(*) FROM snowflake_dim_player
UNION ALL
SELECT 'SNOWFLAKE SCHEMA', 'snowflake_dim_position', COUNT(*) FROM snowflake_dim_position
UNION ALL
SELECT 'SNOWFLAKE SCHEMA', 'snowflake_dim_birth_location', COUNT(*) FROM snowflake_dim_birth_location
UNION ALL
SELECT 'SNOWFLAKE SCHEMA', 'snowflake_dim_count', COUNT(*) FROM snowflake_dim_count
UNION ALL
SELECT 'SNOWFLAKE SCHEMA', 'snowflake_fact_pitch', COUNT(*) FROM snowflake_fact_pitch
UNION ALL
SELECT 'ONE BIG TABLE', 'one_big_table', COUNT(*) FROM one_big_table
ORDER BY schema_type, table_name;
EOF

echo ""
echo "==================================="
echo "Data export to DuckDB completed!"
echo "==================================="
echo ""
echo "Database location: db/duckdb/mlb_data.duckdb"
echo ""
echo "Available tables:"
echo "- Star Schema: star_fact_pitch, star_dim_game, star_dim_player, star_dim_count"
echo "- Snowflake Schema: snowflake_fact_pitch, snowflake_dim_game, snowflake_dim_player, snowflake_dim_position, snowflake_dim_birth_location, snowflake_dim_count"
echo "- One Big Table: one_big_table"
echo ""
echo "To query the data:"
echo "  make query"
echo "  OR"
echo "  duckdb db/duckdb/mlb_data.duckdb"