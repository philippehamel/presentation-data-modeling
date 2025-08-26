import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from datetime import datetime
from etl.statcast_client import StatcastClient
from etl.players_client import PlayersClient
from etl.pipeline import MLBDataPipeline

# Remove these imports for now since they're causing issues
# from io.write import write_to_csv, write_to_parquet
from config.settings import Settings


def main():
    # Define the date range for the data extraction
    start_date = "2025-08-04"
    end_date = "2025-08-06"

    # Initialize and run the pipeline
    pipeline = MLBDataPipeline()
    pipeline.run_pipeline()


if __name__ == "__main__":
    main()
