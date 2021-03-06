# this file should have the end result of having a class that can be run
# with inputs and produce a team
from typing import List, Tuple, NamedTuple, TypeVar, Dict

import pickle
import sys

sys.path.append(".")
# sys.path.append('../models/')

import numpy as np
import pandas as pd
import pulp
import re

import torch

from dataprep import DataPrep
import scoring_functions as sc

M = TypeVar("M")
D = TypeVar("D")


def get_pickled_model(filename: str) -> M:
    # get the pickled file from the directory and convert to the model
    basepath = "../models/"
    with open(basepath + filename, "rb") as f:
        pickled_model = pickle.load(f)
    return pickled_model


def create_player_dict(
    formatted_data: D, filename: str, game: int
) -> Dict[int, Dict[str, np.ndarray]]:
    """formatted_data is a dataprep object that has been instantiated
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
    """
    feat, _ = formatted_data.merge_data()
    cols = feat[feat["rd"] == game].drop(columns=["name", "rd"]).columns

    # create a comprehension from the cols because the one-hot encoder may
    # change the order of the positions based on the order of IDs in the table
    positions_mapping = {
        "goalie": sc.GoalieOrDefender,
        "defense": sc.GoalieOrDefender,
        "midfield": sc.Midfielder,
        "forward": sc.Forward,
    }
    score_type_lookup = {i: positions_mapping[col] for i, col in enumerate(cols[2:6])}

    # random forest model can be uploaded this way
    # model = get_pickled_model(filename)

    # pytorch model upload this way
    # uploading the pytorch model
    model = torch.load(filename)
    model.eval()

    week = formatted_data.get_data_for_predictions(game)

    for k, v in week.items():
        player_score = score_type_lookup[np.argmax(v["vector"][0][1:5])](
            # for use with random forest model
            # *model.predict(v["vector"])[0]
            # for use with pytorch neural network
            *(model.forward(torch.from_numpy(v["vector"][0]).float()).detach().numpy())
        )
        week[k]["predicted_score"] = player_score.score()
        week[k]["position"] = cols[2:6][np.argmax(v["vector"][0][1:5])]
    return week


def create_lp_dicts(
    round_dict: Dict[int, Dict[str, float]]
) -> Tuple[
    Dict[str, Dict[int, str]], Dict[str, Dict[int, float]], Dict[str, Dict[int, str]],
]:
    """Data wrangling with a pandas and dictionary comprehensions to
    organize data into suitable formats to solve the Linear Programming
    Problem.
    Inputs: dict of players and data for the given game.
    Outputs: dict of player by salaries, dict of players by predicted
    points, dict of team by players.
    """
    table = pd.DataFrame(round_dict).T
    table["player_id"] = table.index
    unique_pos = set(v["position"] for k, v in round_dict.items())
    unique_team = set(v["team"] for k, v in round_dict.items())

    salaries = {}
    predicted_points = {}

    for pos in unique_pos:
        available = table[table.position == pos]
        salary = list(
            available[["player_id", "salary"]].set_index("player_id").to_dict().values()
        )[0]
        point = list(
            available[["player_id", "predicted_score"]]
            .set_index("player_id")
            .to_dict()
            .values()
        )[0]
        salaries[pos] = salary
        predicted_points[pos] = point

    team_by_player = {
        team: {k: v["position"] for k, v in round_dict.items() if v["team"] == team}
        for team in unique_team
    }

    return salaries, predicted_points, team_by_player


SQUAD_POS_NUM_AVAILABLE = {
    "goalie": 2,
    "defense": 5,
    "midfield": 5,
    "forward": 3,
}

team_shape_352 = {"goalie": 1, "defense": 3, "midfield": 5, "forward": 2}

subs_shape_352 = {"goalie": 1, "defense": 2, "midfield": 0, "forward": 1}

team_shape_343 = {"goalie": 1, "defense": 3, "midfield": 4, "forward": 3}

subs_shape_343 = {"goalie": 1, "defense": 2, "midfield": 1, "forward": 0}

team_shape_451 = {"goalie": 1, "defense": 4, "midfield": 5, "forward": 1}

subs_shape_451 = {"goalie": 1, "defense": 1, "midfield": 0, "forward": 2}

team_shape_442 = {"goalie": 1, "defense": 4, "midfield": 4, "forward": 2}

subs_shape_442 = {"goalie": 1, "defense": 1, "midfield": 1, "forward": 1}

team_shape_433 = {"goalie": 1, "defense": 4, "midfield": 3, "forward": 3}

subs_shape_433 = {"goalie": 1, "defense": 1, "midfield": 2, "forward": 0}

team_shape_541 = {"goalie": 1, "defense": 5, "midfield": 4, "forward": 1}

subs_shape_541 = {"goalie": 1, "defense": 0, "midfield": 1, "forward": 2}

team_shape_532 = {"goalie": 1, "defense": 5, "midfield": 3, "forward": 2}

subs_shape_532 = {"goalie": 1, "defense": 0, "midfield": 2, "forward": 1}

TEAM_SHAPES = [
    (team_shape_352, subs_shape_352),
    (team_shape_343, subs_shape_343),
    (team_shape_451, subs_shape_451),
    (team_shape_442, subs_shape_442),
    (team_shape_433, subs_shape_433),
    (team_shape_541, subs_shape_541),
    (team_shape_532, subs_shape_532),
]

# constraint for number of players per team

players_team_available = {
    "atlanta_united_fc": 3,
    "chicago_fire_fc": 3,
    "colorado_rapids": 3,
    "columbus_crew_sc": 3,
    "dc_united": 3,
    "fc_cincinnati": 3,
    "fc_dallas": 3,
    "houston_dynamo": 3,
    "inter_miami_cf": 3,
    "la_galaxy": 3,
    "los_angeles_fc": 3,
    "minnesota_united_fc": 3,
    "montreal_impact": 3,
    "nashville_sc": 3,
    "new_england_revolution": 3,
    "new_york_city_fc": 3,
    "new_york_red_bulls": 3,
    "orlando_city_sc": 3,
    "philadelphia_union": 3,
    "portland_timbers": 3,
    "real_salt_lake": 3,
    "san_jose_earthquakes": 3,
    "seattle_sounders_fc": 3,
    "sporting_kansas_city": 3,
    "toronto_fc": 3,
    "vancouver_whitecaps_fc": 3,
}

# the salary amount is constrained to 125
SALARY_CAP = 125


def solve_lp_problem(
    salaries: Dict[int, Dict[str, int]],
    predicted_points: Dict[int, Dict[str, int]],
    teams: Dict[str, Dict[int, str]],
    team_shape: Dict[str, int],
    players_per_team: Dict[str, int],
    salary_cap: int,
) -> float:
    """Create and setup the variables for the Linear Programming problem, 
    and solve it.
    """
    # the player variables are the same whether using the predicted_points
    # dictionary or the salaries dictionary as reference
    _player_variables = {
        k: pulp.LpVariable.dicts(k, v, cat="binary")
        for k, v in predicted_points.items()
    }
    _team_variables = {
        k: pulp.LpVariable.dicts(k, v, cat="binary") for k, v in teams.items()
    }

    prob = pulp.LpProblem("fastbal", pulp.LpMaximize)

    rewards = []
    costs = []
    # create the equations for all player variables by position to show costs, and all player variables by position
    # to show the predicted points. Will set up a constraint for players by position in order to maximize based
    # on the team shape chosen.
    for k, v in _player_variables.items():
        costs += pulp.lpSum([salaries[k][i] * _player_variables[k][i] for i in v])
        rewards += pulp.lpSum(
            [predicted_points[k][i] * _player_variables[k][i] for i in v]
        )
        prob += pulp.lpSum([_player_variables[k][i] for i in v]) <= team_shape[k]

    # create a constraint equation to limit the number of players chose from any single MLS team to 3
    for k, v in _team_variables.items():
        prob += pulp.lpSum([_team_variables[k][i] for i in v]) <= players_per_team[k]

    # this first line sets up the objective, the second line provides the constraint of the salary cap

    prob += pulp.lpSum(costs) <= salary_cap
    prob += pulp.lpSum(rewards)

    prob.solve()
    print(f"Status: {pulp.LpStatus[prob.status]}")

    score = str(prob.objective)
    for v in prob.variables():
        score = score.replace(v.name, str(v.varValue))

    return eval(score)


# using data collected 19Aug2020
# meta_str = "../data/metadata/meta_stats_aug27.csv"
# top_stats_str = "../data/top_stats/top_stats_aug27.csv"
# season_str = "../data/season_stats/season_stats_aug27.csv"
# model_locale = "baseline_rf.pkl"

# data scraped on aug 30th, ahead of week 5 of the season
# meta_str = "../data/metadata/meta_stats_sep4.csv"
# top_stats_str = "../data/top_stats/top_stats_sep4.csv"
# season_str = "../data/season_stats/season_stats_sep4.csv"

# data scraped on Sep 8th, ahead of week 6 of the season
# meta_str = "../data/metadata/meta_stats_sep8.csv"
# top_stats_str = "../data/top_stats/top_stats_sep8.csv"
# season_str = "../data/season_stats/season_stats_sep8.csv"

# data scraped on Sep 8th, removing some injured players
# meta_str = "../data/metadata/meta_stats_injuries_removed_sep8.csv"
# top_stats_str = "../data/top_stats/top_stats_injuries_removed_sep8.csv"
# season_str = "../data/season_stats/season_stats_injuries_removed_sep8.csv"

# data scraped on Sep 14th, ahead of week 7 of the season
# meta_str = "../data/metadata/meta_stats_week7_sep14.csv"
# top_stats_str = "../data/top_stats/top_stats_week7_sep14.csv"
# season_str = "../data/season_stats/season_stats_week7_sep14.csv"

# data scraped Sep 14th, filtered for only players who have played at least 1 minute
meta_str = "../data/metadata/meta_stats_have_played_week7.csv"
top_stats_str = "../data/top_stats/top_stats_have_played_week7.csv"
season_str = "../data/season_stats/season_stats_have_played_week7.csv"

#model_locale = "../models/nn_3layers_sep4.pt"
#model_locale = "../models/nn_3layers_week7_sep14.pt"
model_locale = "../models/nn_2layers_sep17.pt"

dataprepped = DataPrep(meta_str, top_stats_str, season_str)
players = create_player_dict(dataprepped, model_locale, 7)

salaries, pred_points, teams = create_lp_dicts(players)


_variables = {
    k: pulp.LpVariable.dicts(k, v, cat="Binary") for k, v in pred_points.items()
}
_variables_teams = {
    k: pulp.LpVariable.dicts(k, v, cat="Binary") for k, v in teams.items()
}

results = []

for starters, subs in TEAM_SHAPES:

    prob = pulp.LpProblem("fastbal", pulp.LpMaximize)

    rewards = []
    costs = []

    for k, v in _variables.items():
        costs += pulp.lpSum([salaries[k][i] * _variables[k][i] for i in v])
        rewards += pulp.lpSum([pred_points[k][i] * _variables[k][i] for i in v])
        prob += pulp.lpSum([_variables[k][i] for i in v]) <= starters[k]

    for k, v in _variables_teams.items():
        prob += (
            pulp.lpSum([_variables_teams[k][i] for i in v]) <= players_team_available[k]
        )

    prob += pulp.lpSum(rewards)
    prob += pulp.lpSum(costs) <= SALARY_CAP

    prob.solve()
    status = pulp.LpStatus[prob.status]
    # print(f'Status: {pulp.LpStatus[prob.status]}')

    score = str(prob.objective)
    for v in prob.variables():
        score = score.replace(v.name, str(v.varValue))

    # get constraints for the team
    constraints = [str(const) for const in prob.constraints.values()]
    for v in prob.variables():
        constraints = [const.replace(v.name, str(v.varValue)) for const in constraints]
        if v.varValue != 0:
            for const in constraints:
                constraint_readable = " + ".join(re.findall("[0-9\.]*\*1.0", const))

    starter_salaries_total = eval(constraint_readable)

    # to choose the four subs, we go through the LP problem again, first by
    # removing the starters from all the dictionaries we'll use for the LP
    # problem, and then use the subs constraint from the respective starters
    # shape

    team_list = [
        int("".join(re.findall("[\d.]+", v.name)))
        for v in prob.variables()
        if v.varValue > 0
    ]

    subs_salaries = {
        k: {player: sal for player, sal in v.items() if player not in team_list}
        for k, v in salaries.items()
    }

    subs_predicted_points = {
        k: {player: sal for player, sal in v.items() if player not in team_list}
        for k, v in pred_points.items()
    }

    subs_team_by_player = {
        k: {player: pos for player, pos in v.items() if player not in team_list}
        for k, v in teams.items()
    }

    # setup the LP problem for the subs
    _subs_variables = {
        k: pulp.LpVariable.dicts(k, v, cat="Binary")
        for k, v in subs_predicted_points.items()
    }
    _subs_variables_teams = {
        k: pulp.LpVariable.dicts(k, v, cat="Binary")
        for k, v in subs_team_by_player.items()
    }

    subs_prob = pulp.LpProblem("subs_fastbal", pulp.LpMaximize)

    subs_rewards = []
    subs_costs = []

    # create the equations for all player variables by position to show costs, and all player variables by position
    # to show the predicted points. Will set up a constraint for players by position in order to maximize based
    # on the team shape chosen.
    for k, v in _subs_variables.items():
        subs_costs += pulp.lpSum(
            [subs_salaries[k][i] * _subs_variables[k][i] for i in v]
        )
        subs_rewards += pulp.lpSum(
            [subs_predicted_points[k][i] * _subs_variables[k][i] for i in v]
        )
        subs_prob += pulp.lpSum([_subs_variables[k][i] for i in v]) <= subs[k]

    # create a constraint equation to limit the number of players chose from any single MLS team to 3
    for k, v in _subs_variables_teams.items():
        subs_prob += (
            pulp.lpSum([_subs_variables_teams[k][i] for i in v])
            <= players_team_available[k]
        )

    # this first line sets up the objective, the second line provides the constraint of the salary cap
    subs_prob += pulp.lpSum(subs_rewards)
    subs_prob += pulp.lpSum(subs_costs) <= SALARY_CAP - starter_salaries_total

    subs_prob.solve()
    subs_status = pulp.LpStatus[subs_prob.status]

    team_list = [
        int("".join(re.findall("[\d.]+", v.name)))
        for v in prob.variables()
        if v.varValue > 0
    ]

    subs_team_list = [
        int("".join(re.findall("[\d.]+", v.name)))
        for v in subs_prob.variables()
        if v.varValue > 0
    ]
    # print dataframes of each team starters and subs

    meta_df = pd.read_csv(meta_str)
    selected_team = {
        player_id: {
            "name": meta_df[meta_df.ID == player_id].values[0][1],
            "position": players[player_id]["position"],
            "team": players[player_id]["team"],
            "predicted_score": players[player_id]["predicted_score"],
            "salary": players[player_id]["salary"],
        }
        for player_id in team_list
    }

    starters_df = pd.DataFrame(selected_team).T.sort_values(by="position")

    subs_team = {
        player_id: {
            "name": meta_df[meta_df.ID == player_id].values[0][1],
            "position": players[player_id]["position"],
            "team": players[player_id]["team"],
            "predicted_score": players[player_id]["predicted_score"],
            "salary": players[player_id]["salary"],
        }
        for player_id in subs_team_list
    }

    subs_df = pd.DataFrame(subs_team).T.sort_values(by="position")

    playing_shape = "".join((str(v) for v in starters.values()))[1:]

    results.append(
        [
            playing_shape,
            status,
            eval(score),
            starter_salaries_total,
            starters_df,
            subs_df,
        ]
    )

for result in results:
    print(
        f"team shape {result[0]} expected points {result[2]} costs {starters_df.salary.sum() + subs_df.salary.sum()}"
    )
    print(f"starters: \n")
    print(result[4])
    print(f"subs: \n")
    print(result[5])
    print("\n")
for result in results:
    print(
        f"team shape {result[0]} has a score of {result[2]}, a total salary of {starters_df.salary.sum() + subs_df.salary.sum()}, and status {result[1]}"
    )
