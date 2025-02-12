use [London_Bike_Sharing];

--#see London bikes sharing info
select *
from london_bike_data;

--#count table rows
select COUNT(*) as num_rows
from london_bike_data;

--#count uniqe values in the [weather_code] column
select distinct weather_code, COUNT(*) as column_num
from london_bike_data
group by weather_code;

--#count uniqe values in the [season] column
select distinct [season], COUNT(*) as column_num
from london_bike_data
group by [season];

--#specifying the column names that i want to use
EXEC sp_rename 'london_bike_data.timestamp', 'time', 'COLUMN';
EXEC sp_rename 'london_bike_data.cnt', 'count', 'COLUMN';
EXEC sp_rename 'london_bike_data.t1', 'temp_real_C', 'COLUMN';
EXEC sp_rename 'london_bike_data.t2', 'temp_feels_like_C', 'COLUMN';
EXEC sp_rename 'london_bike_data.hum', 'humidity_percent', 'COLUMN';
EXEC sp_rename 'london_bike_data.wind_speed', 'wind_speed_kph', 'COLUMN';
EXEC sp_rename 'london_bike_data.weather_code', 'weather', 'COLUMN';
EXEC sp_rename 'london_bike_data.is_holiday', 'is_holiday', 'COLUMN';
EXEC sp_rename 'london_bike_data.is_weekend', 'is_weekend', 'COLUMN';
EXEC sp_rename 'london_bike_data.season', 'season', 'COLUMN';

--#see London bikes sharing info
select *
from london_bike_data;

--# changing the humidity values to percentage (i.e. a value between 0 and 1)
UPDATE london_bike_data  
SET humidity_percent = humidity_percent / 100;



--#Ensuring Column Data Types are VARCHAR (String)
ALTER TABLE london_bike_data 
ALTER COLUMN season VARCHAR(10);

ALTER TABLE london_bike_data 
ALTER COLUMN weather VARCHAR(50);

--#Check Current Data Format
SELECT DISTINCT season, 
       weather, 
       CAST(season AS VARCHAR) AS season_str,
       CAST(weather AS VARCHAR) AS weather_str
FROM london_bike_data;


--## creating a season dictionary so that we can map the integers 0-3 to the actual written values
UPDATE london_bike_data
SET season = 
    CASE 
        WHEN season = 0 THEN 'Spring'
        WHEN season = 1 THEN 'Summer'
        WHEN season = 2 THEN 'Autumn'
        WHEN season = 3 THEN 'Winter'
    END;


--## creating a weather dictionary so that we can map the integers to the actual written values
UPDATE london_bike_data
SET weather = 
    CASE 
        WHEN weather = 1 THEN 'Clear'
        WHEN weather = 2 THEN 'Scattered clouds'
        WHEN weather = 3 THEN 'Broken clouds'
        WHEN weather = 4 THEN 'Cloudy'
        WHEN weather = 7 THEN 'Rain'
        WHEN weather = 10 THEN 'Rain with thunderstorm'
        WHEN weather = 26 THEN 'Snowfall'
    END;


--# Verify Changes
SELECT DISTINCT season, weather 
FROM london_bike_data;


--#see London bikes sharing info
select *
from london_bike_data;








