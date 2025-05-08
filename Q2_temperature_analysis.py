
# # # # # # # # # # #     for station in warmest_stations:
# # # # # # # # # # #         f.write(f"  {station}\n")
# # # # # # # # # # #     f.write(f"\nCoolest station(s) (avg {min_avg:.2f}°C):\n")
# # # # # # # # # # #     for station in coolest_stations:
# # # # # # # # # # #         f.write(f"  {station}\n")

# # # # # # # # # # # print(f"[✓] Saved warmest and coolest stations to '{extremes_file}'")


# # # # # # # # # # import os
# # # # # # # # # # import pandas as pd

# # # # # # # # # # # Define data directory and output files
# # # # # # # # # # data_dir = "temperatures"
# # # # # # # # # # avg_temp_file = "average_temp.txt"
# # # # # # # # # # range_file = "largest_temp_range_station.txt"
# # # # # # # # # # extremes_file = "warmest_and_coolest_station.txt"

# # # # # # # # # # # Define month order and seasons
# # # # # # # # # # month_order = ["January", "February", "March", "April", "May", "June",
# # # # # # # # # #                "July", "August", "September", "October", "November", "December"]

# # # # # # # # # # season_map = {
# # # # # # # # # #     "Summer": ["December", "January", "February"],
# # # # # # # # # #     "Autumn": ["March", "April", "May"],
# # # # # # # # # #     "Winter": ["June", "July", "August"],
# # # # # # # # # #     "Spring": ["September", "October", "November"]
# # # # # # # # # # }

# # # # # # # # # # # Load all CSV files into one DataFrame
# # # # # # # # # # all_data = []

# # # # # # # # # # # Loop through each file in the directory and load it
# # # # # # # # # # for filename in os.listdir(data_dir):
# # # # # # # # # #     if filename.endswith(".csv"):  # Only process CSV files
# # # # # # # # # #         filepath = os.path.join(data_dir, filename)
# # # # # # # # # #         try:
# # # # # # # # # #             # Read CSV and handle potential delimiter issues (if tab-delimited, use delimiter='\t')
# # # # # # # # # #             df = pd.read_csv(filepath, delimiter=',')  # Adjust delimiter if necessary

# # # # # # # # # #             # Normalize column names (strip whitespace, convert to uppercase)
# # # # # # # # # #             df.columns = df.columns.str.strip().str.upper()

# # # # # # # # # #             # Check required columns
# # # # # # # # # #             required_cols = {"STATION_NAME", "STN_ID", "LAT", "LON"}
# # # # # # # # # #             required_cols.update([m.upper() for m in month_order])  # Add month columns dynamically
# # # # # # # # # #             if not required_cols.issubset(df.columns):
# # # # # # # # # #                 print(f"Skipping {filename}: Missing required columns.")
# # # # # # # # # #                 print(f"Columns found in {filename}: {df.columns.tolist()}")
# # # # # # # # # #                 continue

# # # # # # # # # #             # Keep only necessary columns
# # # # # # # # # #             df = df[["STATION_NAME", "STN_ID", "LAT", "LON"] + [m.upper() for m in month_order]]
# # # # # # # # # #             all_data.append(df)

# # # # # # # # # #         except Exception as e:
# # # # # # # # # #             print(f"Error reading {filename}: {e}")

# # # # # # # # # # # Check if any data was loaded
# # # # # # # # # # if not all_data:
# # # # # # # # # #     print("No valid data found.")
# # # # # # # # # #     exit()

# # # # # # # # # # # Combine all year data
# # # # # # # # # # df_all = pd.concat(all_data, ignore_index=True)

# # # # # # # # # # # Melt the DataFrame: one row per station per month
# # # # # # # # # # df_melted = df_all.melt(
# # # # # # # # # #     id_vars=["STATION_NAME", "STN_ID", "LAT", "LON"],
# # # # # # # # # #     value_vars=[m.upper() for m in month_order],
# # # # # # # # # #     var_name="Month",
# # # # # # # # # #     value_name="Temperature"
# # # # # # # # # # )

# # # # # # # # # # # Drop rows with missing temperatures
# # # # # # # # # # df_melted.dropna(subset=["Temperature"], inplace=True)

# # # # # # # # # # # --- Part 1: Average Temperature by Season ---
# # # # # # # # # # seasonal_avg = {}

# # # # # # # # # # with open(avg_temp_file, "w") as f:
# # # # # # # # # #     for season, months in season_map.items():
# # # # # # # # # #         season_df = df_melted[df_melted["Month"].isin([m.upper() for m in months])]
# # # # # # # # # #         avg_temp = season_df["Temperature"].mean()
# # # # # # # # # #         seasonal_avg[season] = avg_temp
# # # # # # # # # #         f.write(f"{season}: {avg_temp:.2f}°C\n")

# # # # # # # # # # print(f"[✓] Saved seasonal averages to '{avg_temp_file}'")

# # # # # # # # # # # --- Part 2: Station(s) with Largest Temperature Range ---
# # # # # # # # # # range_by_station = df_melted.groupby("STATION_NAME")["Temperature"].agg(["min", "max"])
# # # # # # # # # # range_by_station["range"] = range_by_station["max"] - range_by_station["min"]
# # # # # # # # # # max_range = range_by_station["range"].max()
# # # # # # # # # # largest_range_stations = range_by_station[range_by_station["range"] == max_range].index.tolist()

# # # # # # # # # # with open(range_file, "w") as f:
# # # # # # # # # #     f.write(f"Largest temperature range: {max_range:.2f}°C\n")
# # # # # # # # # #     f.write("Station(s):\n")
# # # # # # # # # #     for station in largest_range_stations:
# # # # # # # # # #         f.write(f"  {station}\n")

# # # # # # # # # # print(f"[✓] Saved stations with largest temperature range to '{range_file}'")

# # # # # # # # # # # --- Part 3: Warmest and Coolest Station(s) by Average ---
# # # # # # # # # # avg_by_station = df_melted.groupby("STATION_NAME")["Temperature"].mean()
# # # # # # # # # # max_avg = avg_by_station.max()
# # # # # # # # # # min_avg = avg_by_station.min()

# # # # # # # # # # warmest_stations = avg_by_station[avg_by_station == max_avg].index.tolist()
# # # # # # # # # # coolest_stations = avg_by_station[avg_by_station == min_avg].index.tolist()

# # # # # # # # # # with open(extremes_file, "w") as f:
# # # # # # # # # #     f.write(f"Warmest station(s) (avg {max_avg:.2f}°C):\n")
# # # # # # # # # #     for station in warmest_stations:
# # # # # # # # # #         f.write(f"  {station}\n")
# # # # # # # # # #     f.write(f"\nCoolest station(s) (avg {min_avg:.2f}°C):\n")
# # # # # # # # # #     for station in coolest_stations:
# # # # # # # # # #         f.write(f"  {station}\n")

# # # # # # # # # # print(f"[✓] Saved warmest and coolest stations to '{extremes_file}'")

# # # # # # # # # # import os
# # # # # # # # # # import pandas as pd

# # # # # # # # # # # Define data directory and output files
# # # # # # # # # # data_dir = "temperatures"
# # # # # # # # # # avg_temp_file = "average_temp.txt"
# # # # # # # # # # range_file = "largest_temp_range_station.txt"
# # # # # # # # # # extremes_file = "warmest_and_coolest_station.txt"

# # # # # # # # # # # Define month order and seasons
# # # # # # # # # # month_order = ["January", "February", "March", "April", "May", "June",
# # # # # # # # # #                "July", "August", "September", "October", "November", "December"]

# # # # # # # # # # season_map = {
# # # # # # # # # #     "Summer": ["December", "January", "February"],
# # # # # # # # # #     "Autumn": ["March", "April", "May"],
# # # # # # # # # #     "Winter": ["June", "July", "August"],
# # # # # # # # # #     "Spring": ["September", "October", "November"]
# # # # # # # # # # }

# # # # # # # # # # # Load all CSV files into one DataFrame
# # # # # # # # # # all_data = []

# # # # # # # # # # # Loop through each file in the directory and load it
# # # # # # # # # # for filename in os.listdir(data_dir):
# # # # # # # # # #     if filename.endswith(".csv"):  # Only process CSV files
# # # # # # # # # #         filepath = os.path.join(data_dir, filename)
# # # # # # # # # #         try:
# # # # # # # # # #             # Read CSV and handle potential tab-delimited format
# # # # # # # # # #             df = pd.read_csv(filepath, delimiter='\t')  # Use '\t' for tab-delimited files

# # # # # # # # # #             # Normalize column names (strip whitespace, convert to uppercase)
# # # # # # # # # #             df.columns = df.columns.str.strip().str.upper()

# # # # # # # # # #             # Check required columns
# # # # # # # # # #             required_cols = {"STATION_NAME", "STN_ID", "LAT", "LON"}
# # # # # # # # # #             required_cols.update([m.upper() for m in month_order])  # Add month columns dynamically
# # # # # # # # # #             if not required_cols.issubset(df.columns):
# # # # # # # # # #                 print(f"Skipping {filename}: Missing required columns.")
# # # # # # # # # #                 print(f"Columns found in {filename}: {df.columns.tolist()}")
# # # # # # # # # #                 continue

# # # # # # # # # #             # Keep only necessary columns
# # # # # # # # # #             df = df[["STATION_NAME", "STN_ID", "LAT", "LON"] + [m.upper() for m in month_order]]
# # # # # # # # # #             all_data.append(df)

# # # # # # # # # #         except Exception as e:
# # # # # # # # # #             print(f"Error reading {filename}: {e}")

# # # # # # # # # # # Check if any data was loaded
# # # # # # # # # # if not all_data:
# # # # # # # # # #     print("No valid data found.")
# # # # # # # # # #     exit()

# # # # # # # # # # # Combine all year data
# # # # # # # # # # df_all = pd.concat(all_data, ignore_index=True)

# # # # # # # # # # # Melt the DataFrame: one row per station per month
# # # # # # # # # # df_melted = df_all.melt(
# # # # # # # # # #     id_vars=["STATION_NAME", "STN_ID", "LAT", "LON"],
# # # # # # # # # #     value_vars=[m.upper() for m in month_order],
# # # # # # # # # #     var_name="Month",
# # # # # # # # # #     value_name="Temperature"
# # # # # # # # # # )

# # # # # # # # # # # Drop rows with missing temperatures
# # # # # # # # # # df_melted.dropna(subset=["Temperature"], inplace=True)

# # # # # # # # # # # --- Part 1: Average Temperature by Season ---
# # # # # # # # # # seasonal_avg = {}

# # # # # # # # # # with open(avg_temp_file, "w") as f:
# # # # # # # # # #     for season, months in season_map.items():
# # # # # # # # # #         season_df = df_melted[df_melted["Month"].isin([m.upper() for m in months])]
# # # # # # # # # #         avg_temp = season_df["Temperature"].mean()
# # # # # # # # # #         seasonal_avg[season] = avg_temp
# # # # # # # # # #         f.write(f"{season}: {avg_temp:.2f}°C\n")

# # # # # # # # # # print(f"[✓] Saved seasonal averages to '{avg_temp_file}'")

# # # # # # # # # # # --- Part 2: Station(s) with Largest Temperature Range ---
# # # # # # # # # # range_by_station = df_melted.groupby("STATION_NAME")["Temperature"].agg(["min", "max"])
# # # # # # # # # # range_by_station["range"] = range_by_station["max"] - range_by_station["min"]
# # # # # # # # # # max_range = range_by_station["range"].max()
# # # # # # # # # # largest_range_stations = range_by_station[range_by_station["range"] == max_range].index.tolist()

# # # # # # # # # # with open(range_file, "w") as f:
# # # # # # # # # #     f.write(f"Largest temperature range: {max_range:.2f}°C\n")
# # # # # # # # # #     f.write("Station(s):\n")
# # # # # # # # # #     for station in largest_range_stations:
# # # # # # # # # #         f.write(f"  {station}\n")

# # # # # # # # # # print(f"[✓] Saved stations with largest temperature range to '{range_file}'")

# # # # # # # # # # # --- Part 3: Warmest and Coolest Station(s) by Average ---
# # # # # # # # # # avg_by_station = df_melted.groupby("STATION_NAME")["Temperature"].mean()
# # # # # # # # # # max_avg = avg_by_station.max()
# # # # # # # # # # min_avg = avg_by_station.min()

# # # # # # # # # # warmest_stations = avg_by_station[avg_by_station == max_avg].index.tolist()
# # # # # # # # # # coolest_stations = avg_by_station[avg_by_station == min_avg].index.tolist()

# # # # # # # # # # with open(extremes_file, "w") as f:
# # # # # # # # # #     f.write(f"Warmest station(s) (avg {max_avg:.2f}°C):\n")
# # # # # # # # # #     for station in warmest_stations:
# # # # # # # # # #         f.write(f"  {station}\n")
# # # # # # # # # #     f.write(f"\nCoolest station(s) (avg {min_avg:.2f}°C):\n")
# # # # # # # # # #     for station in coolest_stations:
# # # # # # # # # #         f.write(f"  {station}\n")

# # # # # # # # # # print(f"[✓] Saved warmest and coolest stations to '{extremes_file}'")




# # # # # # # # # import os
# # # # # # # # # import pandas as pd

# # # # # # # # # # Define data directory and output files
# # # # # # # # # data_dir = "temperatures"
# # # # # # # # # avg_temp_file = "average_temp.txt"
# # # # # # # # # range_file = "largest_temp_range_station.txt"
# # # # # # # # # extremes_file = "warmest_and_coolest_station.txt"

# # # # # # # # # # Define month order and seasons
# # # # # # # # # month_order = ["January", "February", "March", "April", "May", "June",
# # # # # # # # #                "July", "August", "September", "October", "November", "December"]

# # # # # # # # # season_map = {
# # # # # # # # #     "Summer": ["December", "January", "February"],
# # # # # # # # #     "Autumn": ["March", "April", "May"],
# # # # # # # # #     "Winter": ["June", "July", "August"],
# # # # # # # # #     "Spring": ["September", "October", "November"]
# # # # # # # # # }

# # # # # # # # # # Load all CSV files into one DataFrame
# # # # # # # # # all_data = []

# # # # # # # # # # Loop through each file in the directory and load it
# # # # # # # # # for filename in os.listdir(data_dir):
# # # # # # # # #     if filename.endswith(".csv"):  # Only process CSV files
# # # # # # # # #         filepath = os.path.join(data_dir, filename)
# # # # # # # # #         try:
# # # # # # # # #             # Read CSV and handle potential tab-delimited format
# # # # # # # # #             df = pd.read_csv(filepath, delimiter='\t')  # Use '\t' for tab-delimited files

# # # # # # # # #             # Normalize column names (strip whitespace, convert to uppercase)
# # # # # # # # #             df.columns = df.columns.str.strip().str.upper()

# # # # # # # # #             # Check required columns
# # # # # # # # #             required_cols = {"STATION_NAME", "STN_ID", "LAT", "LON"}
# # # # # # # # #             required_cols.update([m.upper() for m in month_order])  # Add month columns dynamically
# # # # # # # # #             if not required_cols.issubset(df.columns):
# # # # # # # # #                 print(f"Skipping {filename}: Missing required columns.")
# # # # # # # # #                 print(f"Columns found in {filename}: {df.columns.tolist()}")
# # # # # # # # #                 continue

# # # # # # # # #             # Keep only necessary columns
# # # # # # # # #             df = df[["STATION_NAME", "STN_ID", "LAT", "LON"] + [m.upper() for m in month_order]]
# # # # # # # # #             all_data.append(df)
# # # # # # # # #             print(f"Processed {filename}")

# # # # # # # # #         except Exception as e:
# # # # # # # # #             print(f"Error reading {filename}: {e}")

# # # # # # # # # # Check if any data was loaded
# # # # # # # # # if not all_data:
# # # # # # # # #     print("No valid data found.")
# # # # # # # # #     exit()

# # # # # # # # # # Combine all year data
# # # # # # # # # df_all = pd.concat(all_data, ignore_index=True)

# # # # # # # # # # Melt the DataFrame: one row per station per month
# # # # # # # # # df_melted = df_all.melt(
# # # # # # # # #     id_vars=["STATION_NAME", "STN_ID", "LAT", "LON"],
# # # # # # # # #     value_vars=[m.upper() for m in month_order],
# # # # # # # # #     var_name="Month",
# # # # # # # # #     value_name="Temperature"
# # # # # # # # # )

# # # # # # # # # # Drop rows with missing temperatures
# # # # # # # # # df_melted.dropna(subset=["Temperature"], inplace=True)

# # # # # # # # # # --- Part 1: Average Temperature by Season ---
# # # # # # # # # seasonal_avg = {}

# # # # # # # # # with open(avg_temp_file, "w") as f:
# # # # # # # # #     for season, months in season_map.items():
# # # # # # # # #         season_df = df_melted[df_melted["Month"].isin([m.upper() for m in months])]
# # # # # # # # #         avg_temp = season_df["Temperature"].mean()
# # # # # # # # #         seasonal_avg[season] = avg_temp
# # # # # # # # #         f.write(f"{season}: {avg_temp:.2f}°C\n")

# # # # # # # # # print(f"[✓] Saved seasonal averages to '{avg_temp_file}'")

# # # # # # # # # # --- Part 2: Station(s) with Largest Temperature Range ---
# # # # # # # # # range_by_station = df_melted.groupby("STATION_NAME")["Temperature"].agg(["min", "max"])
# # # # # # # # # range_by_station["range"] = range_by_station["max"] - range_by_station["min"]
# # # # # # # # # max_range = range_by_station["range"].max()
# # # # # # # # # largest_range_stations = range_by_station[range_by_station["range"] == max_range].index.tolist()

# # # # # # # # # with open(range_file, "w") as f:
# # # # # # # # #     f.write(f"Largest temperature range: {max_range:.2f}°C\n")
# # # # # # # # #     f.write("Station(s):\n")
# # # # # # # # #     for station in largest_range_stations:
# # # # # # # # #         f.write(f"  {station}\n")

# # # # # # # # # print(f"[✓] Saved stations with largest temperature range to '{range_file}'")

# # # # # # # # # # --- Part 3: Warmest and Coolest Station(s) by Average ---
# # # # # # # # # avg_by_station = df_melted.groupby("STATION_NAME")["Temperature"].mean()
# # # # # # # # # max_avg = avg_by_station.max()
# # # # # # # # # min_avg = avg_by_station.min()

# # # # # # # # # warmest_stations = avg_by_station[avg_by_station == max_avg].index.tolist()
# # # # # # # # # coolest_stations = avg_by_station[avg_by_station == min_avg].index.tolist()

# # # # # # # # # with open(extremes_file, "w") as f:
# # # # # # # # #     f.write(f"Warmest station(s) (avg {max_avg:.2f}°C):\n")
# # # # # # # # #     for station in warmest_stations:
# # # # # # # # #         f.write(f"  {station}\n")
# # # # # # # # #     f.write(f"\nCoolest station(s) (avg {min_avg:.2f}°C):\n")
# # # # # # # # #     for station in coolest_stations:
# # # # # # # # #         f.write(f"  {station}\n")

# # # # # # # # # print(f"[✓] Saved warmest and coolest stations to '{extremes_file}'")


# # # # # # # # import os
# # # # # # # # import pandas as pd

# # # # # # # # # Define data directory and output files
# # # # # # # # data_dir = "temperatures"
# # # # # # # # avg_temp_file = "average_temp.txt"
# # # # # # # # range_file = "largest_temp_range_station.txt"
# # # # # # # # extremes_file = "warmest_and_coolest_station.txt"

# # # # # # # # # Define month order and seasons
# # # # # # # # month_order = ["January", "February", "March", "April", "May", "June",
# # # # # # # #                "July", "August", "September", "October", "November", "December"]

# # # # # # # # season_map = {
# # # # # # # #     "Summer": ["December", "January", "February"],
# # # # # # # #     "Autumn": ["March", "April", "May"],
# # # # # # # #     "Winter": ["June", "July", "August"],
# # # # # # # #     "Spring": ["September", "October", "November"]
# # # # # # # # }

# # # # # # # # # Load all CSV files into one DataFrame
# # # # # # # # all_data = []

# # # # # # # # # List all files in the directory to see if all CSV files are detected
# # # # # # # # files_in_directory = os.listdir(data_dir)
# # # # # # # # csv_files = [f for f in files_in_directory if f.endswith(".csv")]
# # # # # # # # print(f"CSV files found in directory: {csv_files}")  # Debugging: List all .csv files found

# # # # # # # # # Loop through each file in the directory and load it
# # # # # # # # for filename in csv_files:
# # # # # # # #     filepath = os.path.join(data_dir, filename)
# # # # # # # #     try:
# # # # # # # #         # Read CSV and handle potential tab-delimited format
# # # # # # # #         print(f"Attempting to read file: {filename}")  # Debugging: Indicate which file is being processed
# # # # # # # #         df = pd.read_csv(filepath, delimiter='\t')  # Use '\t' for tab-delimited files

# # # # # # # #         # Normalize column names (strip whitespace, convert to uppercase)
# # # # # # # #         df.columns = df.columns.str.strip().str.upper()

# # # # # # # #         # Check required columns
# # # # # # # #         required_cols = {"STATION_NAME", "STN_ID", "LAT", "LON"}
# # # # # # # #         required_cols.update([m.upper() for m in month_order])  # Add month columns dynamically
# # # # # # # #         if not required_cols.issubset(df.columns):
# # # # # # # #             print(f"Skipping {filename}: Missing required columns.")
# # # # # # # #             print(f"Columns found in {filename}: {df.columns.tolist()}")
# # # # # # # #             continue

# # # # # # # #         # Keep only necessary columns
# # # # # # # #         df = df[["STATION_NAME", "STN_ID", "LAT", "LON"] + [m.upper() for m in month_order]]
# # # # # # # #         all_data.append(df)
# # # # # # # #         print(f"Processed {filename}")

# # # # # # # #     except Exception as e:
# # # # # # # #         print(f"Error reading {filename}: {e}")

# # # # # # # # # Check if any data was loaded
# # # # # # # # if not all_data:
# # # # # # # #     print("No valid data found.")
# # # # # # # #     exit()

# # # # # # # # # Combine all year data
# # # # # # # # df_all = pd.concat(all_data, ignore_index=True)

# # # # # # # # # Melt the DataFrame: one row per station per month
# # # # # # # # df_melted = df_all.melt(
# # # # # # # #     id_vars=["STATION_NAME", "STN_ID", "LAT", "LON"],
# # # # # # # #     value_vars=[m.upper() for m in month_order],
# # # # # # # #     var_name="Month",
# # # # # # # #     value_name="Temperature"
# # # # # # # # )

# # # # # # # # # Drop rows with missing temperatures
# # # # # # # # df_melted.dropna(subset=["Temperature"], inplace=True)

# # # # # # # # # --- Part 1: Average Temperature by Season ---
# # # # # # # # seasonal_avg = {}

# # # # # # # # with open(avg_temp_file, "w") as f:
# # # # # # # #     for season, months in season_map.items():
# # # # # # # #         season_df = df_melted[df_melted["Month"].isin([m.upper() for m in months])]
# # # # # # # #         avg_temp = season_df["Temperature"].mean()
# # # # # # # #         seasonal_avg[season] = avg_temp
# # # # # # # #         f.write(f"{season}: {avg_temp:.2f}°C\n")

# # # # # # # # print(f"[✓] Saved seasonal averages to '{avg_temp_file}'")

# # # # # # # # # --- Part 2: Station(s) with Largest Temperature Range ---
# # # # # # # # range_by_station = df_melted.groupby("STATION_NAME")["Temperature"].agg(["min", "max"])
# # # # # # # # range_by_station["range"] = range_by_station["max"] - range_by_station["min"]
# # # # # # # # max_range = range_by_station["range"].max()
# # # # # # # # largest_range_stations = range_by_station[range_by_station["range"] == max_range].index.tolist()

# # # # # # # # with open(range_file, "w") as f:
# # # # # # # #     f.write(f"Largest temperature range: {max_range:.2f}°C\n")
# # # # # # # #     f.write("Station(s):\n")
# # # # # # # #     for station in largest_range_stations:
# # # # # # # #         f.write(f"  {station}\n")

# # # # # # # # print(f"[✓] Saved stations with largest temperature range to '{range_file}'")

# # # # # # # # # --- Part 3: Warmest and Coolest Station(s) by Average ---
# # # # # # # # avg_by_station = df_melted.groupby("STATION_NAME")["Temperature"].mean()
# # # # # # # # max_avg = avg_by_station.max()
# # # # # # # # min_avg = avg_by_station.min()

# # # # # # # # warmest_stations = avg_by_station[avg_by_station == max_avg].index.tolist()
# # # # # # # # coolest_stations = avg_by_station[avg_by_station == min_avg].index.tolist()

# # # # # # # # with open(extremes_file, "w") as f:
# # # # # # # #     f.write(f"Warmest station(s) (avg {max_avg:.2f}°C):\n")
# # # # # # # #     for station in warmest_stations:
# # # # # # # #         f.write(f"  {station}\n")
# # # # # # # #     f.write(f"\nCoolest station(s) (avg {min_avg:.2f}°C):\n")
# # # # # # # #     for station in coolest_stations:
# # # # # # # #         f.write(f"  {station}\n")

# # # # # # # # print(f"[✓] Saved warmest and coolest stations to '{extremes_file}'")



# # # # # # # for filename in csv_files:
# # # # # # #     filepath = os.path.join(data_dir, filename)
# # # # # # #     try:
# # # # # # #         print(f"Attempting to read file: {filename}")
# # # # # # #         df = pd.read_csv(filepath, delim_whitespace=True)  # Changed here

# # # # # # #         df.columns = df.columns.str.strip().str.upper()

# # # # # # #         required_cols = {"STATION_NAME", "STN_ID", "LAT", "LON"}
# # # # # # #         required_cols.update([m.upper() for m in month_order])
# # # # # # #         if not required_cols.issubset(df.columns):
# # # # # # #             print(f"Skipping {filename}: Missing required columns.")
# # # # # # #             print(f"Columns found in {filename}: {df.columns.tolist()}")
# # # # # # #             continue

# # # # # # #         df = df[["STATION_NAME", "STN_ID", "LAT", "LON"] + [m.upper() for m in month_order]]
# # # # # # #         all_data.append(df)
# # # # # # #         print(f"Processed {filename}")

# # # # # # #     except Exception as e:
# # # # # # #         print(f"Error reading {filename}: {e}")

# # # # # # import os
# # # # # # import pandas as pd

# # # # # # # Define data directory and output files
# # # # # # data_dir = "temperatures"
# # # # # # avg_temp_file = "average_temp.txt"
# # # # # # range_file = "largest_temp_range_station.txt"
# # # # # # extremes_file = "warmest_and_coolest_station.txt"

# # # # # # # Define month order and seasons
# # # # # # month_order = ["January", "February", "March", "April", "May", "June",
# # # # # #                "July", "August", "September", "October", "November", "December"]

# # # # # # season_map = {
# # # # # #     "Summer": ["December", "January", "February"],
# # # # # #     "Autumn": ["March", "April", "May"],
# # # # # #     "Winter": ["June", "July", "August"],
# # # # # #     "Spring": ["September", "October", "November"]
# # # # # # }

# # # # # # # Load all CSV files into one DataFrame
# # # # # # all_data = []

# # # # # # # List all .csv files in the directory
# # # # # # files_in_directory = os.listdir(data_dir)
# # # # # # csv_files = [f for f in files_in_directory if f.lower().endswith(".csv")]
# # # # # # print(f"CSV files found in directory: {csv_files}")  # Debugging

# # # # # # # Loop through each CSV file
# # # # # # for filename in csv_files:
# # # # # #     filepath = os.path.join(data_dir, filename)
# # # # # #     try:
# # # # # #         print(f"Attempting to read file: {filename}")  # Debugging
# # # # # #         df = pd.read_csv(filepath, delimiter='\t')

# # # # # #         # Normalize column names
# # # # # #         df.columns = df.columns.str.strip().str.upper()

# # # # # #         # Required columns
# # # # # #         required_cols = {"STATION_NAME", "STN_ID", "LAT", "LON"}
# # # # # #         required_cols.update([m.upper() for m in month_order])

# # # # # #         if not required_cols.issubset(set(df.columns)):
# # # # # #             print(f"Skipping {filename}: Missing required columns.")
# # # # # #             print(f"Columns found in {filename}: {df.columns.tolist()}")
# # # # # #             continue

# # # # # #         # Keep only needed columns
# # # # # #         df = df[["STATION_NAME", "STN_ID", "LAT", "LON"] + [m.upper() for m in month_order]]
# # # # # #         all_data.append(df)
# # # # # #         print(f"Successfully processed: {filename}")

# # # # # #     except Exception as e:
# # # # # #         print(f"Error reading {filename}: {e}")

# # # # # # # If no valid data found
# # # # # # if not all_data:
# # # # # #     print("No valid data found in any CSV files.")
# # # # # #     exit()

# # # # # # # Combine all data
# # # # # # df_all = pd.concat(all_data, ignore_index=True)

# # # # # # # Melt to long format
# # # # # # df_melted = df_all.melt(
# # # # # #     id_vars=["STATION_NAME", "STN_ID", "LAT", "LON"],
# # # # # #     value_vars=[m.upper() for m in month_order],
# # # # # #     var_name="Month",
# # # # # #     value_name="Temperature"
# # # # # # )

# # # # # # # Drop missing temperatures
# # # # # # df_melted.dropna(subset=["Temperature"], inplace=True)

# # # # # # # --- Part 1: Average Temperature by Season ---
# # # # # # seasonal_avg = {}
# # # # # # with open(avg_temp_file, "w") as f:
# # # # # #     for season, months in season_map.items():
# # # # # #         season_df = df_melted[df_melted["Month"].isin([m.upper() for m in months])]
# # # # # #         avg_temp = season_df["Temperature"].mean()
# # # # # #         seasonal_avg[season] = avg_temp
# # # # # #         f.write(f"{season}: {avg_temp:.2f}°C\n")
# # # # # # print(f"[✓] Saved seasonal averages to '{avg_temp_file}'")

# # # # # # # --- Part 2: Station(s) with Largest Temperature Range ---
# # # # # # range_by_station = df_melted.groupby("STATION_NAME")["Temperature"].agg(["min", "max"])
# # # # # # range_by_station["range"] = range_by_station["max"] - range_by_station["min"]
# # # # # # max_range = range_by_station["range"].max()
# # # # # # largest_range_stations = range_by_station[range_by_station["range"] == max_range].index.tolist()

# # # # # # with open(range_file, "w") as f:
# # # # # #     f.write(f"Largest temperature range: {max_range:.2f}°C\n")
# # # # # #     f.write("Station(s):\n")
# # # # # #     for station in largest_range_stations:
# # # # # #         f.write(f"  {station}\n")
# # # # # # print(f"[✓] Saved stations with largest temperature range to '{range_file}'")

# # # # # # # --- Part 3: Warmest and Coolest Station(s) by Average ---
# # # # # # avg_by_station = df_melted.groupby("STATION_NAME")["Temperature"].mean()
# # # # # # max_avg = avg_by_station.max()
# # # # # # min_avg = avg_by_station.min()

# # # # # # warmest_stations = avg_by_station[avg_by_station == max_avg].index.tolist()
# # # # # # coolest_stations = avg_by_station[avg_by_station == min_avg].index.tolist()

# # # # # # with open(extremes_file, "w") as f:
# # # # # #     f.write(f"Warmest station(s) (avg {max_avg:.2f}°C):\n")
# # # # # #     for station in warmest_stations:
# # # # # #         f.write(f"  {station}\n")
# # # # # #     f.write(f"\nCoolest station(s) (avg {min_avg:.2f}°C):\n")
# # # # # #     for station in coolest_stations:
# # # # # #         f.write(f"  {station}\n")
# # # # # # print(f"[✓] Saved warmest and coolest stations to '{extremes_file}'")


# # # # # import pandas as pd
# # # # # import matplotlib.pyplot as plt

# # # # # # Load the data
# # # # # df = pd.read_csv('australian_temperatures.csv', sep='\t')

# # # # # # Convert month columns to numeric (in case of any string parsing issues)
# # # # # months = ['January', 'February', 'March', 'April', 'May', 'June',
# # # # #           'July', 'August', 'September', 'October', 'November', 'December']
# # # # # df[months] = df[months].apply(pd.to_numeric, errors='coerce')

# # # # # # Calculate annual average temperature for each station
# # # # # df['AnnualAvgTemp'] = df[months].mean(axis=1)

# # # # # # Plot: Latitude vs Annual Average Temperature
# # # # # plt.figure(figsize=(10, 6))
# # # # # plt.scatter(df['LAT'], df['AnnualAvgTemp'], c='blue', alpha=0.7, edgecolors='k')
# # # # # plt.xlabel('Latitude')
# # # # # plt.ylabel('Annual Average Temperature (°C)')
# # # # # plt.title('Latitude vs. Annual Average Temperature (Australian Stations)')
# # # # # plt.grid(True)
# # # # # plt.gca().invert_xaxis()  # Optional: Flip x-axis so north is on the left
# # # # # plt.tight_layout()
# # # # # plt.show()


# # # # import pandas as pd
# # # # import geopandas as gpd
# # # # import matplotlib.pyplot as plt
# # # # import seaborn as sns
# # # # import os

# # # # data_dir = "C:\\Users\\adity\\OneDrive\\Desktop\\Weather Analysis\\temperatures"

# # # # all_years = []
# # # # for year in range(1986, 2006):
# # # #     file_path = os.path.join(data_dir, f"{year}.csv")
# # # #     print(f"Reading: {file_path}")  # Optional: for debugging
# # # #     df = pd.read_csv(file_path)
# # # #     df['Year'] = year
# # # #     all_years.append(df)

# # # # df_all = pd.concat(all_years, ignore_index=True)


# # # # # Check the structure to confirm column names (you can comment this after confirming)
# # # # print(df_all.columns)

# # # # # Ensure consistent column naming
# # # # df_all.columns = df_all.columns.str.strip().str.lower()

# # # # # Assumes the following column names exist: 'station', 'latitude', 'longitude', 'jan', ..., 'dec'
# # # # # Reshape from wide to long format
# # # # month_order = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
# # # #                'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

# # # # df_melted = pd.melt(
# # # #     df_all,
# # # #     id_vars=['station', 'latitude', 'longitude', 'year'],
# # # #     value_vars=month_order,
# # # #     var_name='month',
# # # #     value_name='temperature'
# # # # )

# # # # # Clean month names and set order
# # # # df_melted['month'] = df_melted['month'].str.capitalize()
# # # # df_melted['month'] = pd.Categorical(df_melted['month'], 
# # # #                                     categories=[m.capitalize() for m in month_order], 
# # # #                                     ordered=True)

# # # # # Compute average temperature for each station per month over all years
# # # # df_avg = df_melted.groupby(['station', 'latitude', 'longitude', 'month'])['temperature'].mean().reset_index()

# # # # # Load Australia shapefile for mapping (ensure you have this, or fetch a base map)
# # # # # Example: from Natural Earth
# # # # aus = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# # # # aus = aus[aus['name'] == 'Australia']

# # # # # Convert to GeoDataFrame
# # # # gdf = gpd.GeoDataFrame(
# # # #     df_avg,
# # # #     geometry=gpd.points_from_xy(df_avg['longitude'], df_avg['latitude']),
# # # #     crs='EPSG:4326'
# # # # )

# # # # # Plot faceted maps by month
# # # # g = sns.FacetGrid(df_avg, col='month', col_wrap=4, height=4, aspect=1.2)

# # # # def facet_map(data, color, **kwargs):
# # # #     ax = plt.gca()
# # # #     aus.plot(ax=ax, color='white', edgecolor='black')
# # # #     sc = ax.scatter(
# # # #         data['longitude'], data['latitude'],
# # # #         c=data['temperature'], cmap='coolwarm', s=20,
# # # #         vmin=df_avg['temperature'].min(), vmax=df_avg['temperature'].max()
# # # #     )
# # # #     ax.set_title(data['month'].iloc[0])
# # # #     ax.set_xlim(110, 155)
# # # #     ax.set_ylim(-45, -10)

# # # # g.map_dataframe(facet_map)
# # # # g.fig.subplots_adjust(right=0.9)
# # # # cbar_ax = g.fig.add_axes([0.92, 0.3, 0.02, 0.4])
# # # # norm = plt.Normalize(vmin=df_avg['temperature'].min(), vmax=df_avg['temperature'].max())
# # # # sm = plt.cm.ScalarMappable(cmap="coolwarm", norm=norm)
# # # # sm.set_array([])
# # # # g.fig.colorbar(sm, cax=cbar_ax, label='Avg Temperature (°C)')

# # # # plt.show()




# # # import os
# # # import pandas as pd

# # # # Directory where the CSV files are stored
# # # data_dir = r"C:\Users\adity\OneDrive\Desktop\Weather Analysis\temperatures"

# # # # Initialize an empty list to store the dataframes
# # # all_data = []

# # # # Loop over the years from 1986 to 2005 and read the CSV files
# # # for year in range(1986, 2006):
# # #     # Construct the file path for each year
# # #     file_path = os.path.join(data_dir, f"{year}.csv")
# # #     print(f"Reading: {file_path}")
    
# # #     # Check if the file exists before attempting to read it
# # #     if os.path.exists(file_path):
# # #         try:
# # #             # Read the CSV file into a dataframe and append it to the list
# # #             df = pd.read_csv(file_path)
# # #             all_data.append(df)
# # #         except Exception as e:
# # #             print(f"Error reading {file_path}: {e}")
# # #     else:
# # #         print(f"File {file_path} not found.")

# # # # If you have successfully read all data, you can combine them
# # # if all_data:
# # #     # Concatenate all dataframes into one
# # #     df_all = pd.concat(all_data, ignore_index=True)
# # #     print("All data loaded successfully.")
# # # else:
# # #     print("No data loaded. Please check if the files exist.")

# # # # Now you can perform operations on df_all, such as data analysis or cleaning
# # # # Example: Display the first few rows of the combined dataframe
# # # print(df_all.head())


# # import pandas as pd
# # import os

# # # Directory containing the temperature data files
# # data_dir = r"C:\Users\adity\OneDrive\Desktop\Weather Analysis\temperatures"

# # # Season mappings
# # seasons = {
# #     'Summer': ['December', 'January', 'February'],
# #     'Autumn': ['March', 'April', 'May'],
# #     'Winter': ['June', 'July', 'August'],
# #     'Spring': ['September', 'October', 'November']
# # }

# # # Function to read all temperature data files
# # def load_data():
# #     files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
# #     all_data = []
# #     for file in files:
# #         file_path = os.path.join(data_dir, file)
# #         print(f"Reading: {file_path}")
# #         df = pd.read_csv(file_path)
# #         all_data.append(df)
# #     return pd.concat(all_data, ignore_index=True)

# # # Function to calculate the average temperature for each season across all years
# # def calculate_seasonal_averages(df):
# #     season_averages = {}
    
# #     # Loop through each season
# #     for season, months in seasons.items():
# #         season_data = df[months].mean(axis=1)
# #         season_avg = season_data.mean()
# #         season_averages[season] = season_avg
    
# #     # Save the results to a file
# #     with open("average_temp.txt", "w") as f:
# #         for season, avg in season_averages.items():
# #             f.write(f"{season}: {avg:.2f}°C\n")
# #     print("Average seasonal temperatures saved to average_temp.txt.")

# # # Function to find the station with the largest temperature range
# # def find_largest_temp_range_station(df):
# #     temp_ranges = {}
    
# #     for index, row in df.iterrows():
# #         station_name = row['STATION_NAME']
# #         temps = row[4:]  # Skip the first four columns (ID, Name, Lat, Lon)
# #         temp_range = temps.max() - temps.min()
# #         temp_ranges[station_name] = temp_range
    
# #     largest_range = max(temp_ranges.values())
# #     stations_with_largest_range = [name for name, range_ in temp_ranges.items() if range_ == largest_range]
    
# #     # Save the results to a file
# #     with open("largest_temp_range_station.txt", "w") as f:
# #         f.write(f"Largest temperature range: {largest_range:.2f}°C\n")
# #         f.write("Stations with the largest temperature range:\n")
# #         for station in stations_with_largest_range:
# #             f.write(f"{station}\n")
# #     print("Largest temperature range station(s) saved to largest_temp_range_station.txt.")

# # # Function to find the warmest and coolest stations
# # def find_warmest_and_coolest_station(df):
# #     avg_temperatures = {}
    
# #     for index, row in df.iterrows():
# #         station_name = row['STATION_NAME']
# #         temps = row[4:]  # Skip the first four columns (ID, Name, Lat, Lon)
# #         avg_temperature = temps.mean()
# #         avg_temperatures[station_name] = avg_temperature
    
# #     warmest_station = max(avg_temperatures, key=avg_temperatures.get)
# #     coolest_station = min(avg_temperatures, key=avg_temperatures.get)
    
# #     # Save the results to a file
# #     with open("warmest_and_coolest_station.txt", "w") as f:
# #         f.write(f"Warmest station: {warmest_station} with {avg_temperatures[warmest_station]:.2f}°C\n")
# #         f.write(f"Coolest station: {coolest_station} with {avg_temperatures[coolest_station]:.2f}°C\n")
# #     print("Warmest and coolest station(s) saved to warmest_and_coolest_station.txt.")

# # # Main function to execute all tasks
# # def main():
# #     # Load all data
# #     df = load_data()
    
# #     # Calculate and save seasonal averages
# #     calculate_seasonal_averages(df)
    
# #     # Find and save the station(s) with the largest temperature range
# #     find_largest_temp_range_station(df)
    
# #     # Find and save the warmest and coolest stations
# #     find_warmest_and_coolest_station(df)

# # if __name__ == "__main__":
# #     main()


# import pandas as pd
# import os

# # Path to the directory containing your CSV files
# data_dir = '/path/to/your/csv_files/'

# # Initialize an empty DataFrame to store combined data
# combined_data = []

# # Loop over the years from 1986 to 2005 to read all CSV files
# for year in range(1986, 2006):
#     file_path = os.path.join(data_dir, f"{year}.csv")
#     if os.path.exists(file_path):
#         # Read each CSV file
#         df = pd.read_csv(file_path)
        
#         # Ensure the dataframe has a column for Station Name, ID, Latitude, Longitude, and Monthly temperatures
#         # Assuming columns are like 'Station Name', 'Station ID', 'Latitude', 'Longitude', 'Jan', 'Feb', ..., 'Dec'
#         if 'Station Name' in df.columns and 'Station ID' in df.columns:
#             # Calculate the Yearly average temperature for each station
#             monthly_columns = df.columns[4:]  # Assuming the first four columns are metadata (Name, ID, Lat, Long)
#             df['Yearly Average'] = df[monthly_columns].mean(axis=1)
            
#             # Add the year column to keep track of which year the data belongs to
#             df['Year'] = year
            
#             # Append the data to the combined_data list
#             combined_data.append(df)

# # Concatenate all the dataframes from 1986 to 2005 into one
# combined_df = pd.concat(combined_data)

# # You can now perform further analysis on the combined_df
# # For example, if you want the yearly average temperature for each station:
# yearly_averages = combined_df.groupby(['Station Name', 'Station ID', 'Year'])['Yearly Average'].mean().reset_index()

# # Display the combined dataframe with the yearly averages
# print(yearly_averages.head())

# # Save the result to a new CSV file
# yearly_averages.to_csv('/path/to/output/yearly_averages.csv', index=False)



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

# # Save largest temperature range station to a text file
# with open('largest_temp_range_station.txt', 'w') as f:
#     f.write(f"Station with the largest temperature range: {max_range_station}\n")

# # Step 4: Find the warmest and coolest station(s)
# avg_temps = {}

# for index, row in data.iterrows():
#     station_name = row['STATION_NAME']
#     station_data = row[4:]
#     avg_temp = station_data.mean()
#     avg_temps[station_name] = avg_temp

# warmest_station = max(avg_temps, key=avg_temps.get)
# coolest_station = min(avg_temps, key=avg_temps.get)

# # Save warmest and coolest station to a text file
# with open('warmest_and_coolest_station.txt', 'w') as f:
#     f.write(f"Warmest station: {warmest_station}\n")
#     f.write(f"Coolest station: {coolest_station}\n")

import pandas as pd
import os

# Initialize the data directory path
data_folder = 'temperatures'  # Change to the correct path of your temperatures folder

# Step 1: Read all CSV files into a list of DataFrames
years = range(1986, 2006)  # From 1986 to 2005
all_data = []

for year in years:
    file_path = os.path.join(data_folder, f"{year}.csv")
    df = pd.read_csv(file_path, delimiter='\t')
    all_data.append(df)

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
    season_avg[season] = season_data.mean(axis=1).mean()  # Average for all stations across all years

# Save season averages to a text file
with open('average_temp.txt', 'w') as f:
    for season, avg_temp in season_avg.items():
        f.write(f"{season}: {avg_temp:.2f}°C\n")

# Step 3: Find the station with the largest temperature range
station_ranges = {}

for index, row in data.iterrows():
    station_name = row['STATION_NAME']
    station_data = row[4:]  # Monthly temperature data
    temp_range = station_data.max() - station_data.min()
    station_ranges[station_name] = temp_range

max_range_station = max(station_ranges, key=station_ranges.get)
max_temp_range = station_ranges[max_range_station]

# Save largest temperature range station with value to a text file
with open('largest_temp_range_station.txt', 'w') as f:
    f.write(f"Station with the largest temperature range: {max_range_station} with a range of {max_temp_range:.2f}°C\n")

# Step 4: Find the warmest and coolest station(s)
avg_temps = {}

for index, row in data.iterrows():
    station_name = row['STATION_NAME']
    station_data = row[4:]
    avg_temp = station_data.mean()
    avg_temps[station_name] = avg_temp

warmest_station = max(avg_temps, key=avg_temps.get)
coolest_station = min(avg_temps, key=avg_temps.get)
warmest_temp = avg_temps[warmest_station]
coolest_temp = avg_temps[coolest_station]

# Save warmest and coolest station with values to a text file
with open('warmest_and_coolest_station.txt', 'w') as f:
    f.write(f"Warmest station: {warmest_station} with an average temperature of {warmest_temp:.2f}°C\n")
    f.write(f"Coolest station: {coolest_station} with an average temperature of {coolest_temp:.2f}°C\n")
