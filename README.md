London Bike Sharing Data Analysis
📌 Project Overview
This project analyzes London bike-sharing data using SQL Server for data processing and analysis, and Tableau for visualization. The goal is to gain insights into bike usage patterns and the impact of various factors such as weather, temperature, and time on bike rentals.
🔗 Dataset
•	Source: Kaggle - London Bike Sharing Dataset
•	Description: The dataset contains bike-sharing data from London, including timestamps, weather conditions, and the number of bike rentals.
📁 Project Structure
📂 London-Bike-Sharing-Analysis
│-- 📁 data                # Raw and processed data files
│-- 📁 sql_scripts         # SQL scripts for data processing
│-- 📁 visualizations      # Tableau dashboards and reports
│-- README.md             # Project documentation
│-- tableau_dashboard.twb # Tableau dashboard file

📌 Categories (Metadata)
•	timestamp - Timestamp field for grouping the data
•	cnt - The count of new bike shares
•	t1 - Real temperature in °C
•	t2 - Temperature in °C "feels like"
•	hum - Humidity in percentage
•	wind_speed - Wind speed in km/h
•	weather_code - Category of the weather
•	is_holiday - Boolean field (1 = holiday, 0 = non-holiday)
•	is_weekend - Boolean field (1 = weekend, 0 = weekday)
•	season - Meteorological season category (0 = Spring, 1 = Summer, 2 = Fall, 3 = Winter)
Weather Code Categories:
•	1 = Clear (mostly clear but may include haze/fog)
•	2 = Scattered clouds / Few clouds
•	3 = Broken clouds
•	4 = Cloudy
•	7 = Rain / Light Rain Shower / Light Rain
•	10 = Rain with Thunderstorm
•	26 = Snowfall
•	94 = Freezing Fog

📊 Analysis Steps
This project follows an end-to-end data analysis process:
The Business Issue
The objective of this analysis is to understand how various factors influence bike-sharing trends in London. Key aspects examined include:
•	Identifying Usage Patterns: Understanding when and how people use bike-sharing services, including peak hours and seasonal trends.
•	Weather Impact on Bike Rentals: Analyzing how different weather conditions affect bike-sharing demand.
•	Effect of Holidays and Weekends: Evaluating whether bike rentals significantly change during holidays and weekends.
•	Temperature and Wind Speed Influence: Exploring how weather conditions impact user decisions.
•	Commuting Trends: Assessing whether bike-sharing is primarily used for commuting purposes based on time-of-day trends.

KPIs for the Dashboard
•	Moving Average Visualization → Tracks the trend of bike rentals over time.
•	Total Rides Visualization → Displays the total number of bike rides.
•	Temperature vs. Wind Speed Heatmap → Analyzes the correlation between temperature, wind speed, and bike rentals.
•	Weather and Hour Bar Charts → Shows the impact of weather conditions and time of day on bike rentals.
EDA (Exploratory Data Analysis) and Feature Engineering

Data Visualization with Tableau
Tableau Dashboard Link:
London Bike Sharing Dashboard
Key Visualizations:
•	Moving average trends
•	Total rides count
•	Correlation heatmap of temperature and wind speed
•	Hourly rental patterns under different weather conditions
📈 Results & Insights
Consistent Growth in Bike Usage: The moving average visualization highlights a steady increase in bike rentals overtime, suggesting a growing adoption of bike-sharing services.
Peak Usage Hours: Most bike rentals occur during morning and evening rush hours (7-9 AM and 5-7 PM), indicating strong use for commuting.
Weather Impact on Rentals: Rainy and stormy weather significantly reduces the number of bike rentals, while clear weather leads to higher ridership.
Wind Speed and Temperature Correlation: Rentals peak at moderate temperatures, but high wind speeds negatively impact ridership.
Seasonal Trends: Summer has the highest number of rentals, whereas winter shows the lowest usage, highlighting the influence of weather conditions on bike-sharing demand.
🛠️ Tools & Technologies
•	SQL Server → Data processing and analysis
•	Excel → Exploratory data analysis and pivot tables
•	Tableau → Interactive dashboards and visualizations

📂 Additional Resources
•	SQL Script File: GitHub SQL File
•	Dashboard link: London Bike Sharing Dashboard
🔗 References
•	Dataset on Kaggle

