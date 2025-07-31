"""
File responsible for merging betting data, game data and weather data
"""
import pandas as pd

team_mapping = {
    "Chicago White Sox": "chicago_white_sox",
    'Pittsburgh Pirates': "pittsburgh_pirates", 
    'St. Louis Cardinals': "st._louis_cardinals",
    'Los Angeles Dodgers': "los_angeles_dodgers", 
    'Cleveland Indians': "cleveland_guardians", 
    'Texas Rangers': "texas_rangers",
    'Tampa Bay Rays': "tampa_bay_rays", 
    'Minnesota Twins': "minnesota_twins", 
    'Toronto Blue Jays': "toronto_blue_jays",
    'Houston Astros': "houston_astros", 
    'Atlanta Braves': "atlanta_braves", 
    'Arizona Diamondbacks': "arizona_diamondbacks",
    'San Francisco Giants': "san_francisco_giants", 
    'Baltimore Orioles': "baltimore_orioles", 
    'Milwaukee Brewers': "milwaukee_brewers",
    'Kansas City Royals': "kansas_city_royals", 
    'New York Mets': "new_york_mets", 
    'Boston Red Sox': "boston_red_sox",
    'Oakland Athletics': "oakland_athletics", 
    'Seattle Mariners': "seattle_mariners", 
    'Miami Marlins': "miami_marlins",
    'Chicago Cubs': "chicago_cubs", 
    'Los Angeles Angels': "los_angeles_angels", 
    'Cincinnati Reds': "cincinnati_reds",
    'Philadelphia Phillies': "philadelphia_phillies", 
    'Detroit Tigers': "detroit_tigers", 
    'Washington Nationals': "washington_nationals",
    'Colorado Rockies': "colorado_rockies", 
    'New York Yankees': "new_york_yankees", 
    'San Diego Padres': "san_diego_padres",
    'Cleveland Guardians': "cleveland_guardians", 
    'Athletics': "oakland_athletics",
}


def merge_data():
    weather_df = pd.read_csv("/Users/hannahwurzel/Desktop/MLB/data/other_data/weather_metadata_copy.csv")
    betting_df = pd.read_csv("/Users/hannahwurzel/Desktop/MLB/data/betting_data/betting_data_transformed.csv")
    weather_df['home_team'] = weather_df['home_team'].replace(team_mapping)
    weather_df['away_team'] = weather_df['away_team'].replace(team_mapping)

    betting_df['date'] = pd.to_datetime(betting_df['date'])
    weather_df['date'] = pd.to_datetime(weather_df['game_date'])

    merged_df = pd.merge(
        betting_df,
        weather_df,
        how='inner', 
        on=['date', 'home_team', 'away_team']
    )

    merged_df = merged_df.drop(['away_score', 'home_score', 'away_team_score', 'home_team_score', 'total_score', 'game_date'], axis=1)
    merged_df.to_csv("/Users/hannahwurzel/Desktop/MLB/data/merged_data.csv", index=False)

merge_data()