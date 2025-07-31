import pandas as pd


def label_result(row):
    '''
    returns the labels for each game
    '''
    total_score = row['home_score'] + row['away_score']
    ou_line = row['over_under']
    if total_score > ou_line:
        return 'Over'
    elif total_score < ou_line:
        return 'Under'
    else:
        return 'Push'
    

# read data and select relevant lines
data = pd.read_csv("/Users/hannahwurzel/Desktop/MLB/data/betting_data/mlb_game_scores_1g_20250713.csv")
data = data[["date", "season", "away_team", "home_team", "away_score", "home_score", "over_under", 
    "dayofweek", "overunder_margin", "home_days_since_previous_game", "home_point_win_streak", "home_point_loss_streak",
    "home_overunder_margin", "home_over_streak", "home_under_streak", "home_overunder_season_avg",
    "away_days_since_previous_game", "away_point_win_streak", "away_point_loss_streak",
    "away_overunder_margin", "away_over_streak", "away_under_streak", "away_overunder_season_avg", "over_line", "under_line",
    "delta_days_since_previous_game", "delta_point_win_streak", "delta_point_loss_streak", "delta_overunder_streak_avg",]]

# cleveland had a name change, so make them all the same
df = data[~data['away_team'].isin(['american_league', 'national_league'])]
df['away_team'] = df['away_team'].replace('cleveland_indians', 'cleveland_guardians')
df['home_team'] = df['home_team'].replace('cleveland_indians', 'cleveland_guardians')

# two games list the home team as 0. remove those.
df = df[df['home_team'] != '0']

# get the labels for each game (over, under, none)
df['target'] = df.apply(label_result, axis=1)

# save off new file
df.to_csv("/Users/hannahwurzel/Desktop/MLB/data/betting_data/betting_data_transformed.csv", index=False)