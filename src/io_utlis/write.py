from typing import Dict
import pandas as pd
import os
from pathlib import Path


def write_to_csv(dataframes: dict, output_dir: str = "data/processed"):
    """Write dataframes to CSV files."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for name, df in dataframes.items():
        file_path = output_path / f"{name}.csv"
        df.to_csv(file_path, index=False)
        print(f"Saved {name} to {file_path}")


def write_to_parquet(dataframes: dict, output_dir: str = "data/processed"):
    """Write dataframes to Parquet files."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for name, df in dataframes.items():
        file_path = output_path / f"{name}.parquet"
        df.to_parquet(file_path, index=False)
        print(f"Saved {name} to {file_path}")


def save_dataframes(dataframes: Dict[str, pd.DataFrame], output_dir: str):
    """Save DataFrames to both CSV and Parquet formats."""
    os.makedirs(output_dir, exist_ok=True)
    write_to_csv(dataframes, output_dir)
    write_to_parquet(dataframes, output_dir)


def main():
    """Main function to export processed data."""
    # Load the existing processed data and save in both formats
    star_dir = "data/processed/star"

    if os.path.exists(star_dir):
        dataframes = {}

        # Load existing CSV files
        for csv_file in Path(star_dir).glob("*.csv"):
            if csv_file.stat().st_size > 0:  # Only load non-empty files
                df_name = csv_file.stem
                try:
                    dataframes[df_name] = pd.read_csv(csv_file)
                    print(f"Loaded {df_name} with {len(dataframes[df_name])} rows")
                except Exception as e:
                    print(f"Error loading {csv_file}: {e}")

        # Save to both CSV and Parquet
        if dataframes:
            write_to_parquet(dataframes, star_dir)
            print(
                f"Successfully exported {len(dataframes)} tables to both CSV and Parquet formats"
            )
        else:
            print("No data found to export")
    else:
        print(f"Directory {star_dir} does not exist")


if __name__ == "__main__":
    main()
