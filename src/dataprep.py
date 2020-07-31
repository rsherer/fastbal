''' functions used for cleaning data that has been scraped from mlssoccer.com
'''
from typing import Tuple, Dict
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder

class DataPrep:
    '''DataPrep takes in three data sets for MLS Fantasy soccer players:
        - Meta data, which is information about the player,
        - Top stats data, which are aggregated or top-level stats for the
        player, and
        - Season stats, which are stats for each player for each game.

        The object will store the transformed, expanded, and combined datasets,
        in order to be used in their respective formats for:
        - data exploration, 
        - numpy arrays that will be used to fit machine learning models used
        for predictions, and
        - dictionaries of player IDs that have a nested dictionary, per player,
        with kyes for position, salary, team, and predicted fantasy points.
        This dictionary will be used for the Linear Programming methodology
        to determined optimized teams.
    '''
    def __init__(self,
                 meta: str,
                 top_stats: str,
                 season: str) -> None:
        self.meta = meta
        self.top_stats = top_stats
        self.season = season
        self.meta_df = None
        self.top_data_df = None
        self.season_features_df = None
        self.season_targets_df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None


    def _encode_categories(self,
                           df: pd.DataFrame,
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

    def meta_feature_prep(self,
                          df: pd.DataFrame) -> pd.DataFrame:
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
                            self._encode_categories(df[['position']])], axis=1)

        features.columns = ['id', 'name', 'salary', 'midfield', 'defense',
                            'goalie', 'forward']

        return features

    def season_feature_target_prep(self,
                                   df: pd.DataFrame) -> \
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
                            self._encode_categories(df[['home_away', 'team']]),
                            self._encode_categories(df[['opponent']], True)],
                            axis=1).rename(columns={'@': 'away', 'vs': 'home'})

        targets = pd.concat([df[['id', 'name', 'rd']],
                            df[df.columns[6:]]], axis=1)

        features.columns = [col.replace(" ", "_").replace(".", "").lower()
                            for col in features.columns]
        targets.columns = [col.lower() for col in targets.columns]

        return features, targets

    def top_stats_feature_prep(self,
                               df: pd.DataFrame) -> pd.DataFrame:
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

    def merge_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        '''Take in file locations as strings for each of meta data, top stats
        data, and season data. Convert to pandas dataframes, clean and transform
        each accordingly, then merge into a data set used for training.
        A tuple is returned with the data set and corresponding target data.
        '''
        self.meta_df = self.meta_feature_prep(pd.read_csv(self.meta))
        self.top_data_df = self.top_stats_feature_prep(pd.read_csv(self.top_stats))
        season_feature_df, season_target_df = \
            self.season_feature_target_prep(pd.read_csv(self.season))

        features_merged = pd.merge(self.meta_df,
                                self.top_data_df,
                                how='outer',
                                left_on='id',
                                right_on='id',
                                suffixes=('', '_top')).merge(
                                                        season_feature_df,
                                                        how='outer',
                                                        left_on='id',
                                                        right_on='id',
                                                        suffixes=('', '_season'))

        features_merged.drop(columns=['name_top', 'name_season'], inplace=True)

        self.season_features_df = features_merged.sort_values(by=['id', 'rd'])
        self.season_targets_df = season_target_df.sort_values(by=['id', 'rd'])

        return self.season_features_df, self.season_targets_df

    def get_data_for_modeling(self,
                              rounds: int) -> \
                                Tuple[np.array, np.array, np.array, np.array]:
        '''Convert features and targets pandas dataframes to numpy arrays to be
        used for modeling.

        Filepaths are where data is stored and used for the data transformations.
        As this is data needs a times series split, the train rounds will retrieve
        data for the beginning part of the season, inclusive the Weeks is an int
        to retrieve data for the first n rounds of the season, inclusive.

        Input -> The rounds that will be used for test data (0 to this round
        number witll be training data, and any rounds above it will be used
        for test data)
        Output -> Tuple[X_train, X_test, y_train, y_test]
        '''
        season_features, season_targets = self.merge_data()

        X_train = season_features[season_features['rd'] <= rounds].copy()
        X_test = season_features[season_features['rd'] > rounds].copy()
        X_train.drop(columns=['id', 'name', 'rd'], inplace=True)
        X_test.drop(columns=['id', 'name', 'rd'], inplace=True)
        self.X_train = X_train.values
        self.X_test = X_test.values

        y_train = season_targets[season_targets['rd'] <= rounds].copy()
        y_test = season_targets[season_targets['rd'] > rounds].copy()
        y_train.drop(columns=['id', 'name', 'rd', 'pts'], inplace=True)
        y_test.drop(columns=['id', 'name', 'rd', 'pts'], inplace=True)
        self.y_train = y_train.values
        self.y_test = y_test.values

        return self.X_train, self.X_test, self.y_train, self.y_test

    def get_data_for_predictions(self, game_week: int) -> \
                                            Dict[int, Dict[str, np.ndarray]]:
        '''This method will combine three data sets into one, and then
        transform the data for the game week argument passed in. The method
        will return a dictionary of dictrionaries that will be used for making
        predictions for each player. 
        '''
        features, _ = self.merge_data()

        features = features[features['rd'] == \
                game_week].drop(columns=['name', 'rd'])

        teams = pd.read_csv(self.meta)
        teams.columns = [col.replace(" ", "_").replace(".", "").lower()
                            for col in teams.columns]
        teams = teams.set_index('id').to_dict('index')

        ids_and_vectors = {player_id: 
            {'vector': features.loc[features['id'] == 
                player_id, :].drop(columns=['id']).values,
             'salary': features.loc[features['id'] == 
                player_id, :].drop(columns=['id']).values[0][0],
             'team': teams[player_id]['team'].replace(" ", "_").replace(".", "").lower()
                }
                    for player_id in features['id']
            }

        return ids_and_vectors


        

