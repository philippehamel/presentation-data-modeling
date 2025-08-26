from typing import List
import pandas as pd

def create_game_dimension(pitch_data: pd.DataFrame) -> pd.DataFrame:
    """
    Create game dimension table from pitch data.
    
    Args:
        pitch_data: DataFrame with pitch-by-pitch data
        
    Returns:
        DataFrame with game dimension data
    """
    games = pitch_data.groupby(['game_pk', 'game_date', 'home_team', 'away_team']).agg({
        'inning': 'max',
        'pitch_number': 'count'
    }).reset_index()
    
    games['game_key'] = range(1, len(games) + 1)
    games['season'] = 2025
    games['game_type'] = 'R'  # Regular season
    games['day_of_week'] = pd.to_datetime(games['game_date']).dt.day_name()
    games['stadium'] = games['home_team'].map({'TOR': 'Rogers Centre', 'COL': 'Coors Field'})
    games['weather_temp'] = 72  # Default temperature
    games['weather_condition'] = 'Clear'
    games['total_pitches'] = games['pitch_number']
    
    return games[['game_key', 'game_pk', 'game_date', 'season', 'game_type', 
                   'home_team', 'away_team', 'stadium', 'day_of_week', 
                   'weather_temp', 'weather_condition', 'total_pitches']]

def create_player_dimension(pitch_data: pd.DataFrame) -> pd.DataFrame:
    """
    Create player dimension table from pitch data.
    
    Args:
        pitch_data: DataFrame with pitch-by-pitch data
        
    Returns:
        DataFrame with player dimension data
    """
    players = pitch_data[['pitcher', 'batter']].melt(value_vars=['pitcher', 'batter'], var_name='role', value_name='player_id')
    players = players.dropna().drop_duplicates()
    
    # Fetch player details from an external source or API
    # This is a placeholder for actual player data fetching logic
    player_details = fetch_player_data(players['player_id'].unique())
    
    return player_details

def create_count_dimension() -> pd.DataFrame:
    """
    Create count dimension table with all possible ball/strike combinations.
    
    Returns:
        DataFrame with count dimension data
    """
    counts = []
    count_key = 1
    
    for balls in range(4):
        for strikes in range(3):
            counts.append({
                'count_key': count_key,
                'balls': balls,
                'strikes': strikes,
                'count_category': categorize_count(balls, strikes)
            })
            count_key += 1
            
    return pd.DataFrame(counts)

def categorize_count(balls: int, strikes: int) -> str:
    """Categorize count as Hitter, Pitcher, or Even."""
    if balls > strikes:
        return 'Hitter'
    elif strikes > balls:
        return 'Pitcher'
    else:
        return 'Even'

def fetch_player_data(player_ids: List[int]) -> pd.DataFrame:
    """
    Fetch player dimension data from MLB API.
    
    Args:
        player_ids: List of MLB player IDs
        
    Returns:
        DataFrame with player information
    """
    # Placeholder for actual API call to fetch player data
    # This should return a DataFrame with player details
    return pd.DataFrame()  # Replace with actual data fetching logic