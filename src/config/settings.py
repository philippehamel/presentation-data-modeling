from pathlib import Path

class Settings:
    def __init__(self):
        # API settings
        self.base_url = "https://statsapi.mlb.com/api/v1"
        self.savant_base = "https://baseballsavant.mlb.com/statcast_search/csv"
        
        # Data directories
        self.data_dir = Path("data")
        self.raw_data_dir = self.data_dir / "raw"
        self.processed_data_dir = self.data_dir / "processed"
        
        # File paths for processed data
        self.star_schema_path = self.processed_data_dir / "star"
        self.snowflake_schema_path = self.processed_data_dir / "snowflake"
        self.one_big_table_path = self.processed_data_dir / "obt"
        
        # DuckDB settings
        self.duckdb_path = Path("db/duckdb")
        
        # Logging settings
        self.log_level = "INFO"
        
        # Other settings
        self.season_year = 2025
        self.start_date = "2025-08-04"
        self.end_date = "2025-08-06"
        
    def get_settings(self):
        return {
            "base_url": self.base_url,
            "savant_base": self.savant_base,
            "data_dir": str(self.data_dir),
            "raw_data_dir": str(self.raw_data_dir),
            "processed_data_dir": str(self.processed_data_dir),
            "star_schema_path": str(self.star_schema_path),
            "snowflake_schema_path": str(self.snowflake_schema_path),
            "one_big_table_path": str(self.one_big_table_path),
            "duckdb_path": str(self.duckdb_path),
            "log_level": self.log_level,
            "season_year": self.season_year,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }