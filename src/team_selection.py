# this file should have the end result of having a class that can be run
# with inputs and produce a team

import pickle
import sys
sys.path.append('.')
#sys.path.append('../models/')

import numpy as np
import pandas as pd
import pulp

import dataprep as dp
import scoring_functions as sc

def get_pickled_model(filename: str) -> object:
    # get the pickled file from the directory and convert to the model
    basepath = '../models/'
    with open(basepath + filename, "rb") as f:
        pickled_model = pickle.load(f)
    return pickled_model

if __name__ == "__main__":
    # data file locations
    meta_str = '../data/metadata/week02/mls_player_metadata_all.csv'
    top_stats_str = '../data/top_stats/week02/player_top_stats_corrected.csv'
    season_str = '../data/season_stats/week02/mls_player_stats_all.csv'
    model_locale = 'baseline_rf.pkl'

    # retrieve pickled model
    model = get_pickled_model(model_locale)

    # get get prepared datasets
    dataprep = dp.DataPrep(meta_str, top_stats_str, season_str)
    week2 = dataprep.get_data_for_predictions(2)

    # the following steps conduct lookups for using the player position to
    # get the proper object that will be used to calculate the player's
    # fantasy score predition

    features, _ = dataprep.merge_data()
    cols = features[features['rd'] == 2].drop(columns=['name', 'rd']).columns

    positions_mapping = {'goalie': sc.GoalieOrDefender,
                        'defense': sc.GoalieOrDefender,
                        'midfield': sc.Midfielder,
                        'forward': sc.Forward}
    position_lookup = {i: positions_mapping[col]
                       for i, col in enumerate(cols[2:6])}

    for k, v in week2.items():
        player_score = position_lookup[np.argmax(
                v['vector'][0][1:5]
            )
        ](
            *model.predict(v['vector'])[0]
        )
        week2[k]['score'] = player_score.score()
        week2[k]['position'] = cols[2:6][np.argmax(np.argmax(
                v['vector'][0][1:5]))]
    print(week2)

    
# first step is to choose a game round, get all eligible players for that
# round, and put them through a pickled model to produce predictions for
# the week.







# from the MLS Fantasy game rules:

# For each match, a squad consists of 15 players wtih a max budget of
# 125 million fantasy dollars.
#
# The squad must have:
#     2 goalkeepers
#     5 defenders
#     5 midfielders
#     3 forwards

# 11 players will be starters, 4 will be on the bench.
# The following formations are valid:

# Starting (D-M-F)                Bench(D-M-F)
# 3-5-2                           2-0-1
# 3-4-3                           2-1-0
# 4-5-1                           1-0-2
# 4-4-2                           1-1-1
# 4-3-3                           1-2-0
# 5-4-1                           0-1-2
# 5-3-2                           0-2-1
