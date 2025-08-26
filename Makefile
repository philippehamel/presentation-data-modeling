# Makefile

.PHONY: all clean fetch build export setup query compare

# Use python3 instead of python for Mac compatibility
PYTHON := python3
VENV_PYTHON := ./venv/bin/python

all: fetch build export

setup:
	@echo "Setting up virtual environment and installing dependencies..."
	$(PYTHON) -m venv venv
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -r requirements.txt

fetch:
	@echo "Fetching data from Baseball Savant and MLB API..."
	./scripts/fetch_and_build.sh

build:
	@echo "Building dimensional models..."
	$(VENV_PYTHON) src/main.py

export:
	@echo "Exporting data to DuckDB..."
	./scripts/export_to_duckdb.sh

query:
	@echo "Opening DuckDB CLI..."
	@echo "Available tables: star_*, snowflake_*, one_big_table"
	@echo "Example queries available in: src/sql/duckdb/queries.sql"
	@echo "Press Ctrl+D to exit"
	@echo ""
	duckdb db/duckdb/mlb_data.duckdb

compare:
	@echo "Running CSV vs Parquet performance comparison..."
	./scripts/compare_csv_parquet.sh

clean:
	@echo "Cleaning up generated files..."
	rm -rf data/processed/* db/duckdb/schema/* data/raw/statcast/* data/raw/mlb/*

clean-all: clean
	@echo "Cleaning up everything including virtual environment..."
	rm -rf venv/
