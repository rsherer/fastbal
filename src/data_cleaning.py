''' functions used for cleaning data that has been scraped from mlssoccer.com
'''
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from typing import List

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

    for i, stat in enumerate(stats):
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
    for i, stat in enumerate(stats):
        if stats[i] == '$/POINT' and stats[i + 2][:2] != 'RD':
            stats[i + 1] = stats[i + 1] + stats[i + 2]
            stats.pop(i + 2)
    return stats
    
    
def encode_categories(df: pd.DataFrame) -> pd.DataFrame:
    '''Will take dataframe and create a one-hot data frame with columns 
    for all unique values in each column of the dataframe.
    '''
    df_cols = [df[col].unique() for col in df.columns]
    
    enc = OneHotEncoder(categories=df_cols, handle_unknown='ignore')
    ohe_cols = [elem for cat in enc.categories for elem in cat]
    
    encoded_df = enc.fit_transform(df.values).toarray()
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
    '''Function will take in a dataframe of meta_data from MLS soccer fantasy 
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
    
    
    features.columns = [col for col in ('id', 'name', 'salary', 'midfield', 
                                        'defense', 'goalie', 'forward')]
    
    return features                                      