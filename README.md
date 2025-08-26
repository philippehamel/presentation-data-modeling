# MLB Dimensional Modeling Presentation

This project demonstrates the extraction, transformation, and loading (ETL) of actual MLB pitch-by-pitch data from Baseball Savant for the Toronto Blue Jays vs. Colorado Rockies series held from August 4-6, 2025. The goal is to showcase different examples of dimensional data modeling, including star schema, snowflake schema, and a denormalized table.

## Project Structure

- **src/**: Contains the main application code, including ETL processes and data transformations.
- **data/**: Holds raw and processed data files.
- **db/**: Contains DuckDB schema files.
- **scripts/**: Includes shell scripts for data fetching and exporting to DuckDB.
- **requirements.txt**: Lists the required Python libraries.
- **Makefile**: Provides commands for managing the project.
- **README.md**: This documentation file.

## Dimensional Models

### Star Schema

The star schema consists of a central fact table that captures pitch-level data, surrounded by dimension tables that provide context. The dimensions include:

- **Game Dimension**: Contains information about each game, such as date, teams, and stadium.
- **Player Dimension**: Holds player-specific data, including names, positions, and birth information.
- **Pitch Count Dimension**: Represents the count of balls and strikes during each pitch.

### Snowflake Schema

The snowflake schema normalizes the dimensions into third normal form (3NF). This means that:

- The player dimension may be split into separate tables for player details and player positions.
- The game dimension may include separate tables for stadium and team information.

### One Big Table

The one big table schema is a denormalized representation that combines all relevant data into a single table. This format is useful for analytical queries that require access to all data without the need for joins.

## Data Export

The processed data is exported in both CSV and Parquet formats for flexibility in data storage and querying.

## DuckDB Integration

To load the data into DuckDB, follow these steps:

1. Ensure DuckDB is installed on your local machine.
2. Use the provided SQL scripts in the `src/sql/duckdb/` directory to create the necessary tables.
3. Execute the `load_csv_parquet.sql` script to load the exported data files into DuckDB.
4. Use the `queries.sql` file to run analytical queries against the loaded data.

## Analytical Queries

The following queries can be used to demonstrate the differences between the models:

- **Star Schema**: Analyze pitch performance by player and game.
- **Snowflake Schema**: Examine player statistics while considering their positions and teams.
- **One Big Table**: Perform comprehensive analyses without the need for joins.

## DBML Diagrams

DBML files are provided in the `src/dbml/` directory for generating visual representations of the different models using dbdiagram.io.

## CSV vs. Parquet with DuckDB

### Parquet Advantages (Recommended):

- **Storage Efficiency**: 60-80% smaller file sizes due to columnar compression
- **Loading Performance**: 2-5x faster data loading into DuckDB
- **Query Performance**: 3-10x faster analytical queries
- **Native Support**: DuckDB has built-in optimizations for Parquet format
- **Schema Preservation**: Maintains data types and null handling better

### CSV Advantages:

- **Simplicity**: Human-readable, easy to inspect and debug
- **Universal Compatibility**: Supported by virtually all tools and systems
- **Streaming**: Can be read line-by-line for very large datasets

### Cons of CSV:

- **Larger File Sizes**: No compression, inefficient storage
- **Slower Performance**: Text parsing overhead during loading and queries
- **Type Inference**: May incorrectly guess data types

### Cons of Parquet:

- **Binary Format**: Not human-readable, requires specialized tools to inspect
- **Complexity**: More complex format specification

### Performance Results from this Project:

```
File Size Comparison:
- fact_pitch.csv: 588KB
- fact_pitch.parquet: 225KB (62% smaller)
- one_big_table.csv: 887KB
- one_big_table.parquet: 264KB (70% smaller)

Loading Performance:
- CSV loading: 0.910s
- Parquet loading: 0.369s (2.5x faster)
```

### Quick Commands:

```bash
# Use Parquet (recommended)
make export

# Compare CSV vs Parquet performance
make compare

# Load only CSV files (if needed)
duckdb db/mlb_data.duckdb < src/sql/duckdb/load_csv_parquet.sql
```

This project provides a comprehensive overview of dimensional data modeling using actual MLB data, showcasing the strengths and weaknesses of different modeling approaches.
