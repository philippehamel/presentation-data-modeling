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
    weather_condition VARCHAR(50) NOT NULL,
    total_pitches INTEGER NOT NULL
);

CREATE TABLE dim_player (
    player_key INTEGER PRIMARY KEY,
    mlb_id INTEGER NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    birth_city VARCHAR(50),
    birth_country VARCHAR(50),
    height VARCHAR(10),
    weight INTEGER,
    bats VARCHAR(1),
    throws VARCHAR(1),
    position VARCHAR(10),
    mlb_debut_date DATE,
    current_team_id INTEGER,
    active_status BOOLEAN,
    effective_date DATE,
    expiration_date DATE,
    is_current BOOLEAN
);

CREATE TABLE dim_count (
    count_key INTEGER PRIMARY KEY,
    balls INTEGER NOT NULL,
    strikes INTEGER NOT NULL,
    count_category VARCHAR(10) NOT NULL
);

CREATE TABLE fact_pitches (
    game_key INTEGER NOT NULL,
    pitcher_key INTEGER NOT NULL,
    batter_key INTEGER NOT NULL,
    count_key INTEGER NOT NULL,
    pitch_number INTEGER NOT NULL,
    inning INTEGER NOT NULL,
    inning_topbot VARCHAR(3) NOT NULL,
    outs_when_up INTEGER NOT NULL,
    pitch_type VARCHAR(10) NOT NULL,
    release_speed FLOAT NOT NULL,
    release_spin_rate FLOAT NOT NULL,
    pfx_x FLOAT NOT NULL,
    pfx_z FLOAT NOT NULL,
    plate_x FLOAT NOT NULL,
    plate_z FLOAT NOT NULL,
    zone INTEGER NOT NULL,
    type VARCHAR(1) NOT NULL,
    events VARCHAR(50),
    launch_speed FLOAT,
    launch_angle FLOAT,
    hit_distance_sc FLOAT,
    PRIMARY KEY (game_key, pitch_number),
    FOREIGN KEY (game_key) REFERENCES dim_game(game_key),
    FOREIGN KEY (pitcher_key) REFERENCES dim_player(player_key),
    FOREIGN KEY (batter_key) REFERENCES dim_player(player_key),
    FOREIGN KEY (count_key) REFERENCES dim_count(count_key)
);