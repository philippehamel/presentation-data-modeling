import sys
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from etl.pipeline import MLBDataPipeline


def main():
    pipeline = MLBDataPipeline()
    pipeline.run_pipeline()


if __name__ == "__main__":
    main()
