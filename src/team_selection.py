# this file should have the end result of having a class that can be run
# with inputs and produce a team
from typing import List, Tuple, NamedTuple, TypeVar, Dict

import pickle
import sys
sys.path.append('.')
#sys.path.append('../models/')

import numpy as np
import pandas as pd
import pulp

from dataprep import DataPrep
import scoring_functions as sc

M = TypeVar('M')
D = TypeVar('D')

def get_pickled_model(filename: str) -> M:
    # get the pickled file from the directory and convert to the model
    basepath = '../models/'
    with open(basepath + filename, "rb") as f:
        pickled_model = pickle.load(f)
    return pickled_model

def create_player_dict(formatted_data: D, 
                           filename: str,
                           game: int) -> Dict[int, Dict[str, np.ndarray]]:
    '''formatted_data is a dataprep object that has been instantiated
    with meta, top_stats, and season data files.
    rd is the round of the season for the match that will be used for
    predictions and choosing a team.
    filename is a string for the pickled model used for predicting the 
    weekly statistics.

    The output is a dictionary with player ids as keys, and the values are
    a dictionary with the following keys and values:
        'vector' - this is the predicted stats in for the player that week
        'salary' - the player's salary
        'team' - the player's team
        'predicted_score' - this is the sum of fantasy points when running
        the 'vector' value through the respective position scoring rubrik
        'position' - the player's position, as in 'defense', 'forward', etc
    '''
    feat, _ = formatted_data.merge_data()
    cols = feat[feat['rd'] == game].drop(columns=['name', 'rd']).columns
    
    # create a comprehension from the cols because the one-hot encoder may
    # change the order of the positions based on the order of IDs in the table
    positions_mapping = {'goalie': sc.GoalieOrDefender,
                         'defense': sc.GoalieOrDefender,
                         'midfield': sc.Midfielder,
                         'forward': sc.Forward}
    score_type_lookup = {i: positions_mapping[col]
                         for i, col in enumerate(cols[2:6])}    

    model = get_pickled_model(filename)
    week = formatted_data.get_data_for_predictions(game)

    for k, v in week.items():
        player_score = score_type_lookup[np.argmax(
                v['vector'][0][1:5]
            )
        ](
            *model.predict(v['vector'])[0]
        )
        week[k]['predicted_score'] = player_score.score()
        week[k]['position'] = cols[2:6][np.argmax(
                v['vector'][0][1:5])]
    return week

def create_lp_dicts(round_dict: Dict[int, Dict[str, float]]) -> \
                            Tuple[
                                Dict[str, Dict[int, str]],
                                Dict[str, Dict[int, float]],
                                Dict[str, Dict[int, str]]]:
    '''Data wrangling with a pandas and dictionary comprehensions to
    organize data into suitable formats to solve the Linear Programming
    Problem.
    Inputs: dict of players and data for the given game.
    Outputs: dict of player by salaries, dict of players by predicted
    points, dict of team by players.
    '''
    table = pd.DataFrame(round_dict).T
    table['player_id'] = table.index
    unique_pos = set(v['position'] for k, v in round_dict.items())
    unique_team = set(v['team'] for k, v in round_dict.items())

    salaries = {}
    predicted_points = {}

    for pos in unique_pos:
        available = table[table['position'] == pos]
        salary = list(available[['player_id', 'salary']].set_index('player_id').to_dict().values())[0]
        point = list(available[['player_id', 'predicted_score']].set_index('player_id').to_dict().values())[0]
        salaries[pos] = salary
        predicted_points[pos] = point

    team_by_player = {
        team: {
            k: v['position'] 
            for k, v in round_dict.items() if v['team'] == team
        }
        for team in unique_team
    }

    return salaries, predicted_points, team_by_player

def lp_problem:
    pass

if __name__ == "__main__":
    # data file locations
    meta_str = '../data/metadata/week02/mls_player_metadata_all.csv'
    top_stats_str = '../data/top_stats/week02/player_top_stats_corrected.csv'
    season_str = '../data/season_stats/week02/mls_player_stats_all.csv'
    model_locale = 'baseline_rf.pkl'    

    # get player dictionary
    dataprepped = DataPrep(meta_str, top_stats_str, season_str)
    players = create_player_dict(dataprepped, model_locale, 2)

    # get LP dictionaries
    salaries, pred_points, teams = create_lp_dicts(players)
