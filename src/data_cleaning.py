''' functions used for cleaning data that has been scraped from mlssoccer.com
'''
from typing import List, Tuple
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder


def remove_negative_scores(stats: List[str]) -> List[str]:
    '''Check row of game summary data for a hyphen to indicate a negative
    score, and then update the row for the negative score for the game, and
    correct the length of the row to match the rest of the table.

    Created specifically used for cleaning up the data from top_stats, but
    should be explored to see if it can be repurposed.
    '''
    cols = ['GAMES PLAYED', 'AVG FANTASY PTS', 'TOTAL FANTASY PTS',
            'LAST WK FANTASY PTS', '3 WK AVG', '5 WK AVG', 'HIGH SCORE',
            'LOW SCORE', 'OWNED BY', '$/POINT', 'RD 2 RANK', 'SEASON RANK']

    for i, _ in enumerate(stats):
        if stats[i] == '-' and stats[i + 1] not in cols:
            stats[i + 1] = '-' + stats[i + 1]
            stats[i:] = stats[(i + 1):]
    return stats

def concat_salary_per_point(stats: List[str]) -> List[str]:
    '''Used for top stats data, to clean up possibility of raw scraped text
    having a cost per point bisected by a ','. The function will look to see
    if the cost per point field is following by more than 1 field, concat the
    two and remove the trailing field.
    '''
    for i, _ in enumerate(stats):
        if stats[i] == '$/POINT' and stats[i + 2][:2] != 'RD':
            stats[i + 1] = stats[i + 1] + stats[i + 2]
            stats.pop(i + 2)
    return stats

def encode_categories(df: pd.DataFrame,
                      name_col: bool = False) -> pd.DataFrame:
    '''Will take dataframe and create a one-hot data frame with columns for
    all unique values in each column of the dataframe.

    name_col=True will put 'OPPONENT' in front of the opponent team, to
    differentiate it from the player's team.
    '''
    df_cols = [df[col].unique() for col in df.columns]

    enc = OneHotEncoder(categories=df_cols, handle_unknown='ignore')
    encoded_df = enc.fit_transform(df.values).toarray()

    if name_col:
        ohe_cols = enc.get_feature_names(df.columns)
    else:
        ohe_cols = [elem for cat in enc.categories for elem in cat]

    encoded_df = pd.DataFrame(encoded_df, columns=ohe_cols)

    return encoded_df

def calculate_ytd_fantasy_points(df: pd.DataFrame,
                                 game_week: int) -> pd.DataFrame:
    '''Calculate the year-to-date fantasy points for each player up to and
    including the current round. To used specifically with the season stats
    dataframe for MLS soccer.
    '''
    necessary_columns = ['rd', 'name', 'id', 'pts']
    for col in necessary_columns:
        assert col in df.columns, f"col '{col}' not in list of: {df.columns}"

    # this returns a df with a mulitindex of ['id', 'name']
    return df[df['rd'] <= game_week][['name',
                                      'id',
                                      'pts']].groupby(['id', 'name']).sum()

def meta_feature_prep(df: pd.DataFrame) -> pd.DataFrame:
    '''Takes in a dataframe of meta_data from MLS soccer fantasy
    soccer and creates features from the dataframe for use in modeling.
    Preparation includes one-hot encoding the position column, and renaming
    the column from initials to the positions.
    '''

    df.columns = [col.lower() for col in df.columns]

    necessary_columns = ['id', 'name', 'position', 'salary']
    for col in necessary_columns:
        assert col in df.columns, f"col '{col}' not in list of: {df.columns}"

    features = pd.concat([df[['id', 'name', 'salary']],
                          encode_categories(df[['position']])], axis=1)

    features.columns = ['id', 'name', 'salary', 'midfield', 'defense',
                        'goalie', 'forward']

    return features

def season_feature_target_prep(df: pd.DataFrame) -> \
                               Tuple[pd.DataFrame, pd.DataFrame]:
    '''Takes in season_data for all players for all weeks of the
    season and convert team, opponent, and the home_away field of the match to
    one-hot encoded features.

    The remaining columns starting with 'pts' (points) ending with 'wf' (was
    fouled) will become the targets table that can be used for modeling.
    '''

    df.columns = [col.lower() for col in df.columns]

    # alter the type for all the numerical columns (which will be the target
    # array) to int from str
    for col in df.iloc[:, 7:].columns:
        df[col] = df[col].str.replace('-', '0', regex=False).astype(int)

    features = pd.concat([df[['id', 'name', 'rd']],
                          encode_categories(df[['home_away', 'team']]),
                          encode_categories(df[['opponent']], True)],
                         axis=1).rename(columns={'@': 'away', 'vs': 'home'})

    targets = pd.concat([df[['id', 'name', 'rd']],
                         df[df.columns[6:]]], axis=1)

    features.columns = [col.replace(" ", "_").lower()
                        for col in features.columns]
    targets.columns = [col.lower() for col in targets.columns]

    return features, targets

def top_stats_feature_prep(df: pd.DataFrame) -> pd.DataFrame:
    '''Function will take in top stats data in the player profile for each
    player and convert the table data to a features dataframe. Depending
    on modeling, features will be added or removed.
    '''
    df = df.rename(columns={'$/point': 'price_per_point'})
    df['last_wk_fantasy_pts'] = \
        df['last_wk_fantasy_pts'].str.replace('DNP', '0', regex=False)
    df['last_wk_fantasy_pts'] = \
        pd.to_numeric(df['last_wk_fantasy_pts'], errors='coerce')
    df['last_wk_fantasy_pts'].fillna(0, inplace=True)
    df['owned_by'] = df['owned_by'] / 100
    df['price_per_point'] = \
        df['price_per_point'].str.replace('[^0-9]', '', regex=True).astype(int)
    df['price_per_point'] = df['price_per_point'] / 1000

    return df[['id', 'name', 'games_played', 'avg_fantasy_pts',
               'total_fantasy_pts', 'high_score', 'low_score', 'owned_by',
               'price_per_point']]

def merge_data(meta_data_filepath: str,
               top_data_filepath: str,
               season_data_filepath: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    '''Take in file locations as strings for each of meta data, top stats
    data, and season data. Convert to pandas dataframes, clean and transform
    each accordingly, then merge into a data set used for training.
    A tuple is returned with the data set and corresponding target data.
    '''
    meta_data = meta_feature_prep(pd.read_csv(meta_data_filepath))
    top_data = top_stats_feature_prep(pd.read_csv(top_data_filepath))
    season_data_feat, season_data_target = season_feature_target_prep(
        pd.read_csv(season_data_filepath))

    features_merged = pd.merge(meta_data,
                               top_data,
                               how='outer',
                               left_on='id',
                               right_on='id',
                               suffixes=('', '_top')).merge(season_data_feat,
                                                    how='outer',
                                                    left_on='id',
                                                    right_on='id',
                                                    suffixes=('', '_season'))

    features_merged.drop(columns=['name_top', 'name_season'], inplace=True)

    features_merged = features_merged.sort_values(by=['id', 'rd'])
    season_data_target = season_data_target.sort_values(by=['id', 'rd'])

    return features_merged, season_data_target

def get_data_for_modeling(meta_data_filepath: str,
               top_data_filepath: str,
               season_data_filepath: str) -> Tuple[np.array, np.array]:
    '''Convert features and targets pandas dataframes to numpy arrays to be
    used for modeling.
    '''
    features, targets = merge_data(meta_data_filepath,
                                  top_data_filepath,
                                  season_data_filepath)

    features.drop(columns=['id', 'name', 'rd'], inplace=True)
    features = features.values
    targets.drop(columns=['id', 'name', 'rd', 'pts'], inplace=True)
    targets = targets.values
    
    return features, targets