CREATE TABLE dim_game (
    game_key INTEGER PRIMARY KEY,
    game_pk INTEGER NOT NULL,
    game_date DATE NOT NULL,
    season INTEGER NOT NULL,
    game_type VARCHAR(1) NOT NULL,
    home_team VARCHAR(3) NOT NULL,
    away_team VARCHAR(3) NOT NULL,
    stadium VARCHAR(50) NOT NULL,
    day_of_week VARCHAR(10) NOT NULL,
    weather_temp INTEGER NOT NULL,
    weather_condition VARCHAR(20) NOT NULL,
    total_pitches INTEGER NOT NULL
);

CREATE TABLE dim_player (
    player_key INTEGER PRIMARY KEY,
    mlb_id INTEGER NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    birth_city VARCHAR(50) NOT NULL,
    birth_country VARCHAR(50) NOT NULL,
    height VARCHAR(10) NOT NULL,
    weight INTEGER NOT NULL,
    bats VARCHAR(1) NOT NULL,
    throws VARCHAR(1) NOT NULL,
    position VARCHAR(10) NOT NULL,
    mlb_debut_date DATE NOT NULL,
    current_team_id INTEGER NOT NULL,
    active_status BOOLEAN NOT NULL,
    effective_date DATE NOT NULL,
    expiration_date DATE NOT NULL,
    is_current BOOLEAN NOT NULL
);

CREATE TABLE dim_count (
    count_key INTEGER PRIMARY KEY,
    balls INTEGER NOT NULL,
    strikes INTEGER NOT NULL,
    count_category VARCHAR(10) NOT NULL
);