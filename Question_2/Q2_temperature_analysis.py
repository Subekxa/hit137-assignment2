
# import pandas as pd
# import os

# # Initialize the data directory path
# data_folder = 'temperatures'  # Change to the correct path of your temperatures folder

# # Step 1: Read all CSV files into a list of DataFrames
# years = range(1986, 2006)  # From 1986 to 2005
# all_data = []

# for year in years:
#     file_path = os.path.join(data_folder, f"{year}.csv")
#     df = pd.read_csv(file_path, delimiter='\t')
#     all_data.append(df)

# # Combine all the data into one DataFrame
# data = pd.concat(all_data, axis=0, ignore_index=True)

# # Step 2: Calculate the average temperature for each season (across all years)
# season_months = {
#     'Summer': ['December', 'January', 'February'],
#     'Autumn': ['March', 'April', 'May'],
#     'Winter': ['June', 'July', 'August'],
#     'Spring': ['September', 'October', 'November']
# }

# season_avg = {}

# for season, months in season_months.items():
#     season_data = data[months]
#     season_avg[season] = season_data.mean(axis=1).mean()  # Average for all stations across all years

# # Save season averages to a text file
# with open('average_temp.txt', 'w') as f:
#     for season, avg_temp in season_avg.items():
#         f.write(f"{season}: {avg_temp:.2f}°C\n")

# # Step 3: Find the station with the largest temperature range
# station_ranges = {}

# for index, row in data.iterrows():
#     station_name = row['STATION_NAME']
#     station_data = row[4:]  # Monthly temperature data
#     temp_range = station_data.max() - station_data.min()
#     station_ranges[station_name] = temp_range

# max_range_station = max(station_ranges, key=station_ranges.get)
# max_temp_range = station_ranges[max_range_station]

# # Save largest temperature range station with value to a text file
# with open('largest_temp_range_station.txt', 'w') as f:
#     f.write(f"Station with the largest temperature range: {max_range_station} with a range of {max_temp_range:.2f}°C\n")

# # Step 4: Find the warmest and coolest station(s)
# avg_temps = {}

# for index, row in data.iterrows():
#     station_name = row['STATION_NAME']
#     station_data = row[4:]
#     avg_temp = station_data.mean()
#     avg_temps[station_name] = avg_temp

# warmest_station = max(avg_temps, key=avg_temps.get)
# coolest_station = min(avg_temps, key=avg_temps.get)
# warmest_temp = avg_temps[warmest_station]
# coolest_temp = avg_temps[coolest_station]

# # Save warmest and coolest station with values to a text file
# with open('warmest_and_coolest_station.txt', 'w') as f:
#     f.write(f"Warmest station: {warmest_station} with an average temperature of {warmest_temp:.2f}°C\n")
#     f.write(f"Coolest station: {coolest_station} with an average temperature of {coolest_temp:.2f}°C\n")


import pandas as pd
import os

# Get the absolute path to the folder containing this script
base_dir = os.path.dirname(__file__)

# Correct path to the temperatures folder
data_folder = os.path.join(base_dir, 'temperatures')

# Step 1: Read all CSV files into a list of DataFrames
years = range(1986, 2006)  # From 1986 to 2005
all_data = []

for year in years:
    file_path = os.path.join(data_folder, f"{year}.csv")
    try:
        df = pd.read_csv(file_path, delimiter='\t')
        all_data.append(df)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Combine all the data into one DataFrame
data = pd.concat(all_data, axis=0, ignore_index=True)

# Step 2: Calculate the average temperature for each season (across all years)
season_months = {
    'Summer': ['December', 'January', 'February'],
    'Autumn': ['March', 'April', 'May'],
    'Winter': ['June', 'July', 'August'],
    'Spring': ['September', 'October', 'November']
}

season_avg = {}

for season, months in season_months.items():
    season_data = data[months]
    season_avg[season] = season_data.mean(axis=1).mean()  # Avg across months and all stations

# Save season averages to a text file
with open(os.path.join(base_dir, 'average_temp.txt'), 'w') as f:
    for season, avg_temp in season_avg.items():
        f.write(f"{season}: {avg_temp:.2f}°C\n")

# Step 3: Find the station with the largest temperature range
station_ranges = {}

for index, row in data.iterrows():
    station_name = row['STATION_NAME']
    monthly_data = row[4:]  # Assuming first 4 columns are metadata
    temp_range = monthly_data.max() - monthly_data.min()
    station_ranges[station_name] = temp_range

max_range_station = max(station_ranges, key=station_ranges.get)
max_temp_range = station_ranges[max_range_station]

# Save result to file
with open(os.path.join(base_dir, 'largest_temp_range_station.txt'), 'w') as f:
    f.write(f"Station with the largest temperature range: {max_range_station} with a range of {max_temp_range:.2f}°C\n")

# Step 4: Find the warmest and coolest stations
avg_temps = {}

for index, row in data.iterrows():
    station_name = row['STATION_NAME']
    monthly_data = row[4:]
    avg_temp = monthly_data.mean()
    avg_temps[station_name] = avg_temp

warmest_station = max(avg_temps, key=avg_temps.get)
coolest_station = min(avg_temps, key=avg_temps.get)

# Save warmest and coolest station to file
with open(os.path.join(base_dir, 'warmest_and_coolest_station.txt'), 'w') as f:
    f.write(f"Warmest station: {warmest_station} with an average temperature of {avg_temps[warmest_station]:.2f}°C\n")
    f.write(f"Coolest station: {coolest_station} with an average temperature of {avg_temps[coolest_station]:.2f}°C\n")
