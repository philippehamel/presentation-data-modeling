-- ==============================================
-- MLB Dimensional Modeling - Example Queries
-- ==============================================
-- Show all available tables
.tables -- ==============================================
-- STAR SCHEMA QUERIES
-- ==============================================
-- 1. Get total pitches thrown by each pitcher
SELECT p.full_name as pitcher_name,
    COUNT(*) AS total_pitches,
    AVG(f.release_speed) as avg_speed
FROM star_fact_pitch f
    JOIN star_dim_player p ON f.pitcher = p.player_id
GROUP BY p.full_name,
    p.player_id
ORDER BY total_pitches DESC
LIMIT 10;
-- 2. Pitch count analysis (balls vs strikes)
SELECT c.count_display,
    c.count_category,
    COUNT(*) as pitch_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM star_fact_pitch f
    JOIN star_dim_count c ON f.balls = c.balls
    AND f.strikes = c.strikes
GROUP BY c.count_display,
    c.count_category,
    c.balls,
    c.strikes
ORDER BY c.balls,
    c.strikes;
-- 3. Game-by-game pitch summary
SELECT g.game_date,
    g.home_team,
    g.away_team,
    COUNT(*) as total_pitches,
    COUNT(DISTINCT f.pitcher) as pitchers_used
FROM star_fact_pitch f
    JOIN star_dim_game g ON f.game_pk = g.game_pk
GROUP BY g.game_date,
    g.home_team,
    g.away_team,
    g.game_pk
ORDER BY g.game_date;
-- ==============================================
-- SNOWFLAKE SCHEMA QUERIES  
-- ==============================================
-- 4. Players by position (normalized)
SELECT pos.primary_position,
    COUNT(*) as player_count
FROM snowflake_dim_player p
    JOIN snowflake_dim_position pos ON p.primary_position = pos.primary_position
GROUP BY pos.primary_position
ORDER BY player_count DESC;
-- 5. Players by birth country (normalized)
SELECT bl.birth_country,
    COUNT(*) as player_count,
    STRING_AGG(p.full_name, ', ') as players
FROM snowflake_dim_player p
    JOIN snowflake_dim_birth_location bl ON p.birth_city = bl.birth_city
    AND p.birth_country = bl.birth_country
GROUP BY bl.birth_country
ORDER BY player_count DESC;
-- 6. Pitching performance by country of origin
SELECT bl.birth_country,
    COUNT(*) as pitches_thrown,
    AVG(f.release_speed) as avg_velocity,
    COUNT(DISTINCT f.pitcher) as pitcher_count
FROM snowflake_fact_pitches f
    JOIN snowflake_dim_player p ON f.pitcher = p.player_id
    JOIN snowflake_dim_birth_location bl ON p.birth_city = bl.birth_city
    AND p.birth_country = bl.birth_country
GROUP BY bl.birth_country
ORDER BY pitches_thrown DESC;
-- ==============================================
-- ONE BIG TABLE QUERIES (No Joins Needed!)
-- ==============================================
-- 7. Simple pitch analysis without joins
SELECT pitch_type,
    COUNT(*) as pitch_count,
    AVG(release_speed) as avg_speed,
    MIN(release_speed) as min_speed,
    MAX(release_speed) as max_speed
FROM one_big_table
WHERE release_speed IS NOT NULL
GROUP BY pitch_type
ORDER BY pitch_count DESC;
-- 8. Team performance summary
SELECT home_team,
    COUNT(*) as pitches_at_home,
    COUNT(DISTINCT game_pk) as home_games,
    AVG(release_speed) as avg_pitch_speed
FROM one_big_table
GROUP BY home_team
ORDER BY pitches_at_home DESC;
-- 9. Inning-by-inning breakdown
SELECT inning,
    COUNT(*) as total_pitches,
    AVG(release_speed) as avg_speed,
    COUNT(
        CASE
            WHEN type = 'S' THEN 1
        END
    ) as strikes,
    COUNT(
        CASE
            WHEN type = 'B' THEN 1
        END
    ) as balls
FROM one_big_table
WHERE inning <= 9
GROUP BY inning
ORDER BY inning;
-- ==============================================
-- COMPARISON QUERIES
-- ==============================================
-- 10. Performance comparison: Star vs One Big Table
-- (Same logic, different table structures)
-- Star Schema approach:
SELECT 'Star Schema' as approach,
    COUNT(*) as total_records
FROM star_fact_pitch f
    JOIN star_dim_player p ON f.pitcher = p.player_id
WHERE p.primary_position = 'Pitcher';
-- One Big Table approach:
SELECT 'One Big Table' as approach,
    COUNT(*) as total_records
FROM one_big_table
WHERE pitcher_primary_position = 'Pitcher';
-- ==============================================
-- SAMPLE QUERIES TO GET STARTED
-- ==============================================
-- Quick data exploration:
SELECT 'Star Schema Tables' as info,
    COUNT(*) as count
FROM star_fact_pitch
UNION ALL
SELECT 'Snowflake Schema Tables',
    COUNT(*)
FROM snowflake_fact_pitches
UNION ALL
SELECT 'One Big Table Rows',
    COUNT(*)
FROM one_big_table;
-- Show some sample data:
SELECT *
FROM star_dim_player
LIMIT 5;
SELECT *
FROM one_big_table
LIMIT 3;
f.is_hit = TRUE
GROUP BY p.position
ORDER BY avg_launch_speed DESC;
-- One Big Table Queries
-- 5. Get the total number of home runs hit in the one big table
SELECT COUNT(*) AS total_home_runs
FROM one_big_table
WHERE is_home_run = TRUE;
-- 6. Get the average pitch speed for strikes and balls in the one big table
SELECT type,
    AVG(release_speed) AS avg_speed
FROM one_big_table
GROUP BY type;