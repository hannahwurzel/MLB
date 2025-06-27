"""
File responsible for adding weather data to existing metadata file.
"""
import requests
import csv
import pandas as pd
from tqdm import tqdm

metadata = pd.read_csv("/Users/hannahwurzel/Desktop/MLB/metadata.csv")
locs = pd.read_json("/Users/hannahwurzel/Desktop/MLB/game_locations.json")


metadata["max_temp_C"] = None
metadata["min_temp_C"] = None
metadata["precipitation_mm"] = None
metadata["max_wind_speed_kmh"] = None
metadata["dominant_wind_dir_deg"] = None


for index, row in tqdm(metadata.iterrows(), desc="Adding weather data"):
    stadium = row['game_loc']
    lat = locs[stadium]['lat']
    lon = locs[stadium]['lon']
    date = row['game_date']

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": date,
        "end_date": date,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "windspeed_10m_max",
            "winddirection_10m_dominant"
        ],
        "timezone": "auto"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        daily = data.get("daily", {})
        if daily and "time" in daily and daily["time"]:
            metadata.at[index, "max_temp_C"] = daily["temperature_2m_max"][0]
            metadata.at[index, "min_temp_C"] = daily["temperature_2m_min"][0]
            metadata.at[index, "precipitation_mm"] = daily["precipitation_sum"][0]
            metadata.at[index, "max_wind_speed_kmh"] = daily["windspeed_10m_max"][0]
            metadata.at[index, "dominant_wind_dir_deg"] = daily["winddirection_10m_dominant"][0]

    except Exception as e:
        print(f"Error on row {index}: {e}")


metadata.to_csv("metadata/metadata_with_weather.csv", index=False)
print("Weather data merged and saved.")
