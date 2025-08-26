#!/bin/bash

# MLB Dimensional Modeling Data Pipeline
# Fetches pitch-by-pitch data from Baseball Savant and player data from MLB API
# for Blue Jays vs Rockies series (Aug 4-6, 2025)

echo "==================================="
echo "MLB Data Pipeline - Fetch & Build"
echo "==================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo "Step 1: Fetching Statcast pitch data from Baseball Savant..."
echo "         - Downloading pitch-by-pitch data for TOR vs COL series"
echo "         - Date range: August 4-6, 2025"

echo "Step 2: Fetching player data from MLB API..."
echo "         - Getting detailed player information for all pitchers and batters"
echo "         - Saving raw API responses to data/raw/mlb/"

echo "Step 3: Building dimensional models..."
echo "         - Star Schema: fact table with dimension tables"
echo "         - Snowflake Schema: normalized dimensions (3NF)"
echo "         - One Big Table: fully denormalized"

echo ""
echo "Starting data pipeline..."
python src/main.py

if [ $? -eq 0 ]; then
    echo ""
    echo "==================================="
    echo "Data fetching and processing completed successfully!"
    echo "==================================="
    echo ""
    echo "Generated files:"
    echo "- Raw Statcast data: data/raw/statcast/"
    echo "- Raw MLB API data: data/raw/mlb/"
    echo "- Star schema: data/processed/star/"
    echo "- Snowflake schema: data/processed/snowflake/"
    echo "- One big table: data/processed/obt/"
    echo ""
    echo "Next steps:"
    echo "- Run 'make export' to load data into DuckDB"
    echo "- Run 'make query' to start querying the data"
else
    echo ""
    echo "==================================="
    echo "Error occurred during data processing!"
    echo "==================================="
    echo "Please check the error messages above and try again."
    exit 1
fi