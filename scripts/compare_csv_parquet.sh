#!/bin/bash

echo "=============================================="
echo "CSV vs Parquet Performance Comparison"
echo "=============================================="

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Database path
DUCKDB_DB_PATH="db/duckdb/mlb_data_comparison.duckdb"

# Create a clean database for comparison
rm -f "$DUCKDB_DB_PATH"

echo ""
echo "Testing CSV loading performance..."
echo "=================================="

# Time CSV loading
time duckdb "$DUCKDB_DB_PATH" <<EOF
CREATE OR REPLACE TABLE csv_fact_pitch AS SELECT * FROM read_csv_auto('data/processed/star/fact_pitch.csv');
CREATE OR REPLACE TABLE csv_one_big_table AS SELECT * FROM read_csv_auto('data/processed/obt/one_big_table.csv');
SELECT 'CSV Loading Complete' as status, COUNT(*) as rows FROM csv_fact_pitch;
EOF

echo ""
echo "Testing Parquet loading performance..."
echo "======================================"

# Time Parquet loading
time duckdb "$DUCKDB_DB_PATH" <<EOF
CREATE OR REPLACE TABLE parquet_fact_pitch AS SELECT * FROM read_parquet('data/processed/star/fact_pitch.parquet');
CREATE OR REPLACE TABLE parquet_one_big_table AS SELECT * FROM read_parquet('data/processed/obt/one_big_table.parquet');
SELECT 'Parquet Loading Complete' as status, COUNT(*) as rows FROM parquet_fact_pitch;
EOF

echo ""
echo "File size comparison:"
echo "===================="
echo "CSV files:"
ls -lh data/processed/star/fact_pitch.csv data/processed/obt/one_big_table.csv
echo ""
echo "Parquet files:"
ls -lh data/processed/star/fact_pitch.parquet data/processed/obt/one_big_table.parquet

echo ""
echo "Query performance comparison:"
echo "============================"

echo "CSV query timing:"
time duckdb "$DUCKDB_DB_PATH" -c "SELECT pitch_type, COUNT(*) FROM csv_fact_pitch GROUP BY pitch_type ORDER BY COUNT(*) DESC;"

echo ""
echo "Parquet query timing:"
time duckdb "$DUCKDB_DB_PATH" -c "SELECT pitch_type, COUNT(*) FROM parquet_fact_pitch GROUP BY pitch_type ORDER BY COUNT(*) DESC;"

echo ""
echo "=============================================="
echo "Summary:"
echo "- Parquet files are typically 60-80% smaller"
echo "- Parquet loading is usually 2-5x faster"
echo "- Parquet queries are often 3-10x faster"
echo "- DuckDB has native Parquet support"
echo "=============================================="

# Clean up
rm -f "$DUCKDB_DB_PATH"
