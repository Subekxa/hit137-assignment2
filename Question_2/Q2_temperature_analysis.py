import pandas as pd
import os

# Get the absolute path to the folder containing this script
# This allows the script to work regardless of where it's executed from
base_dir = os.path.dirname(__file__)

# Correct path to the 'temperatures' folder where the data files are stored
# This ensures the code always looks for the folder in the right location
data_folder = os.path.join(base_dir, 'temperatures')

# Step 1: Read all CSV files into a list of DataFrames
# Loop through the years 1986 to 2005 and load the corresponding CSV files into a list
years = range(1986, 2006)  # From 1986 to 2005
all_data = []  # This will store the DataFrames for all the years

# Loop through each year, read the corresponding file, and add the DataFrame to the list
for year in years:
    file_path = os.path.join(data_folder, f"{year}.csv")  # Construct the file path
    try:
        # Read the CSV file using tab as delimiter and store the DataFrame in the list
        df = pd.read_csv(file_path, delimiter='\t')
        all_data.append(df)
    except FileNotFoundError:
        # If the file is not found, print a message with the file path
        print(f"File not found: {file_path}")
    except Exception as e:
        # Print any other errors that might occur while reading the file
        print(f"Error reading {file_path}: {e}")

# Combine all the DataFrames from different years into one big DataFrame
# The rows from all years will be stacked on top of each other
data = pd.concat(all_data, axis=0, ignore_index=True)

# Step 2: Calculate the average temperature for each season (across all years)
# Define which months belong to which season
season_months = {
    'Summer': ['December', 'January', 'February'],
    'Autumn': ['March', 'April', 'May'],
    'Winter': ['June', 'July', 'August'],
    'Spring': ['September', 'October', 'November']
}

season_avg = {}  # Dictionary to store the average temperatures for each season

# Loop through each season and calculate the average temperature for that season
for season, months in season_months.items():
    # Select the columns for the months in the current season
    season_data = data[months]
    
    # Calculate the mean temperature for all stations across the season and all years
    season_avg[season] = season_data.mean(axis=1).mean()

# Save the average temperature for each season into a text file
with open(os.path.join(base_dir, 'average_temp.txt'), 'w') as f:
    for season, avg_temp in season_avg.items():
        f.write(f"{season}: {avg_temp:.2f}°C\n")  # Write each season's average temperature

# Step 3: Find the station with the largest temperature range
station_ranges = {}  # Dictionary to store the temperature range for each station

# Loop through each row in the data (each row corresponds to a station)
for index, row in data.iterrows():
    station_name = row['STATION_NAME']  # Get the station name from the row
    monthly_data = row[4:]  # Get the monthly temperature data (ignoring metadata columns)
    
    # Calculate the temperature range: the difference between the max and min temperature
    temp_range = monthly_data.max() - monthly_data.min()
    
    # Store the temperature range for this station in the dictionary
    station_ranges[station_name] = temp_range

# Find the station with the largest temperature range
max_range_station = max(station_ranges, key=station_ranges.get)
max_temp_range = station_ranges[max_range_station]

# Save the station with the largest temperature range to a text file
with open(os.path.join(base_dir, 'largest_temp_range_station.txt'), 'w') as f:
    f.write(f"Station with the largest temperature range: {max_range_station} with a range of {max_temp_range:.2f}°C\n")

# Step 4: Find the warmest and coolest stations based on average temperatures
avg_temps = {}  # Dictionary to store the average temperature for each station

# Loop through each row (station) and calculate the average temperature
for index, row in data.iterrows():
    station_name = row['STATION_NAME']  # Get the station name
    monthly_data = row[4:]  # Get the temperature data for that station
    avg_temp = monthly_data.mean()  # Calculate the average temperature for the station
    avg_temps[station_name] = avg_temp  # Store the average temperature for the station

# Find the warmest and coolest stations
warmest_station = max(avg_temps, key=avg_temps.get)  # Find the station with the highest average temp
coolest_station = min(avg_temps, key=avg_temps.get)  # Find the station with the lowest average temp

# Save the warmest and coolest stations along with their temperatures to a text file
with open(os.path.join(base_dir, 'warmest_and_coolest_station.txt'), 'w') as f:
    f.write(f"Warmest station: {warmest_station} with an average temperature of {avg_temps[warmest_station]:.2f}°C\n")
    f.write(f"Coolest station: {coolest_station} with an average temperature of {avg_temps[coolest_station]:.2f}°C\n")
