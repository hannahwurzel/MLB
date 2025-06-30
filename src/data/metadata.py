"""
To retrieve the metadata add get_metadata(<YEAR>) to the bottom of this file and run metadata.py

To clean and combine the metadata add combine_metadata() to the bottom of this file and run metadata.pys

"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random
import tqdm
from sklearn import preprocessing
import os

def get_metadata(year: int):
    """
    Gets the metadata from each game from a certain year

    year : int
        year of game metadata wanted
    """
    base_url = "https://www.baseball-reference.com/"
    schedule_url = f"{base_url}leagues/majors/{year}-schedule.shtml"
    soup = BeautifulSoup(requests.get(schedule_url).text, "html.parser")

    game_links = [a['href'] for a in soup.find_all('a', string='Boxscore')]

    months = {"January", "February", "March", "April", "May", "June", 
          "July", "August", "September", "October", "November", "December"}
    
    game_metadata = []
    for i, link in tqdm.tqdm(enumerate(game_links), total=len(game_links), desc="Getting Metadata"):
        try:
            s = BeautifulSoup(requests.get(base_url + link).text, "html.parser")
            metadata = s.find("div", class_="scorebox_meta")
            game_date = venue = None
            for div in metadata.find_all("div"):
                text = div.get_text(strip=True)
                if ',' in text and any(month in text for month in months):
                    game_date = text
                elif text.startswith("Venue"):
                    venue = text.split(":", 1)[-1].strip()
            game_metadata.append([game_date, venue])

            score_data = s.find("div", class_="scorebox")
            teams = score_data.find_all("div", recursive=False)[:2] 
            for team in teams:
                name = team.find("strong").find("a").text
                score = team.find("div", class_="score").text
                game_metadata[i].extend([name,score])
            time.sleep(random.uniform(3, 5))
        except:
            break

    metadata_df = pd.DataFrame(game_metadata)
    metadata_df.columns = ["game_date", "game_loc", "away_team", "away_team_score", "home_team", "home_team_score"]
    metadata_df.to_csv(f'metadata_{year}_{i}.csv', index=False)


def clean_date(val):  
    """
    Removes the time value from a date

    val : pd.DateTime
        date (and time) value
    """
    try:
        return pd.to_datetime(val).date()
    except:
        return val 


def clean_metadata(file: str):
    """
    Transforms the metadata for use in ML models.

    file : str
        metadata file path
    """
    data = pd.read_csv(file)
    df = pd.DataFrame(data)

    df['game_date'] = pd.to_datetime(df['game_date'])
    df['game_date_ordinal'] = df['game_date'].map(pd.Timestamp.toordinal)

    label_encoder = preprocessing.LabelEncoder()
    df['game_loc']= label_encoder.fit_transform(df['game_loc'])
    df['away_team'] = label_encoder.fit_transform(df['away_team'])
    df['home_team'] = label_encoder.fit_transform(df['home_team'])

    return df

def combine_metadata(directory_path: str = "/Users/hannahwurzel/Desktop/MLB/metadata"):
    """
    Combines the metadata files, transforms it and saves it to the same location as the metadata

    directory_path : str
        location of metadata file paths
    """
    combined_metadata_list = []

    for filename in os.listdir(directory_path):
        if filename.startswith("metadata"):
            file_path = os.path.join(directory_path, filename)
            #df = clean_metadata(file_path)
            df = pd.read_csv(f"{directory_path}/{filename}")
            print(f"cleaned file: {filename}")
            combined_metadata_list.append(df)

    combined_metadata = pd.concat(combined_metadata_list, ignore_index=True)
    combined_metadata['game_date'] = combined_metadata['game_date'].apply(clean_date)
    #combined_metadata['game_date'] = combined_metadata['game_date'].apply(lambda x: x.toordinal())
    combined_metadata['total_score'] = combined_metadata['away_team_score'] + combined_metadata['home_team_score']
    combined_metadata.to_csv(f"{directory_path}/all_metadata.csv", index=False)

    return

df = clean_metadata("/Users/hannahwurzel/Desktop/MLB/metadata/metadata.csv")
df.to_csv("/Users/hannahwurzel/Desktop/MLB/metadata/metadata_transformed.csv")