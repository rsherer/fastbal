# fastbal -> FAntasy Soccer Team By ALgorithm
Using machine learning and linear programming to choose an MLS Fantasy soccer team.

You can find the current standings for the 2020 season [HERE.](https://github.com/rsherer/fastbal/blob/master/2020_season_standings.md)

## This project includes the following sections:

  * [Overview](#overview)
  * [Data Collection](#data-collection)
  * [Data transformation for use in modeling](#data-transforms)
  * [Modeling and cross validation](#modeling-and-cross-validation)
  * [Linear Programming to guide team selection based on model predictions](#linear-programming)
  * [Acknowledgements](#acknowledgments)

## Overview

Fantasy sports are a common manner for casual (or not so - some people can take it 
very seriously, and wager hundreds or even thousands of dollars in private leagues)
fans of a sport to participate alongside the sport in question. Participants will
join a league, and through various rules, construct teams of players in that league,
and earn points based on the specific rules for the fantasy league. Fantasy Football
and Fantasy Baseball are probably the largest fantasy leagues in the US.

For several years, I have played in fantasy soccer leagues, with players for the English Premier
League, and here in the US with Major League Soccer (MLS). I was spending many hours
each week trying to choose a team, and decided to build a model to automate that process.

MLS Fantasy Soccer [rules](https://fantasy.mlssoccer.com/#help/game-rules) detail everyting
from selecting a team, to constraints for composition of the team (ie salary, number of players by
position, etc), and dates for each round of the season. Each player is assigned an MLS
team, a position, and a salary. Key constraints for constructing a team are:

  * Each team must have 11 starters and 4 subs
  * A team must have 1 goalie that starts, and 1 goalie sub
  * A team must have 5 defenders, of which between 3 and 5 start each week
  * A team must have 5 midfielders, of which between 3 and 5 start each week
  * A team must have 3 forwards, of which between 1 and 3 start each weak
  * The salary of the 15 players must be less than or equal to $125 million
  * Each fantasy team must have a mix of players, such that no more than 3 players
  come from any single MLS team.

For each game week, each player accrues stats in 25 categories, most of which add points
to a players weekly total (goals, passes, blocks, etc), and a few of which subtract
points (goals allowed, yellow cards, red cards). The total points for each player
is tallied each week, and the sum of all the starters is what determines the fantasy
team's point total.

## Data Collection

Once an account has been created, training data and target data can be collected by 
scraping data from the [MLS Fantasy Soccer](https://fantasy.mlssoccer.com) website.

First a player list of ids can be constructed with the following steps:

```
import player_ids as pi
import player_data_scraper as pds

login, pwd = 'your_mls_fantasy_login', 'your_fantasy_password'
driver = pi.mls_fantasy_login(login, pwd)
player_list = pi.get_player_ids_listform(driver)
```

As of October 2020, there is a quirk that Miguel Ibarra (who doesn't play much, which is
a bummer because he's a great player and I'm a Sounders fan), Tanner Beason of
the San Jose Earthquakes, and Yony Gonazalez, have some data that is not inputted properly on the MLS 
Fantasy stats pages. For the scraper to work properly, I remove them from the player list to continue.

Each player is a list of strings in the format `id, name, team`, so the following scripts
will remove them from the variable `player_list`:

```
for idx, player in enumerate(player_list):
    if "Ibarra" in player[1]:
        ibarra = idx
player_list.pop(ibarra)

for idx, player in enumerate(player_list):
    if "Beason" in player[1]:
        beason = idx
player_list.pop(beason)

for idx, player in enumerate(player_list):
    if "Y. Gonzalez" in player[1]:
        ygonzalex = idx
player_list.pop(ygonzalez)
```

After which, to scrape the website, the following will script will scrape the meta data,
top level data, and season stats for each player for weeks 1 through 5 in this example:

```
meta, top, weekly = pds.cycle_all_player_ids(driver, player_list, 1, 5)
```

Save the variables variables to `.csv` files, and then prepending the global variables:
`TOP_STATS_COLUMNS`, `SEASON_STATS_COLUMNS`, `META_STATS_COLUMNS` available in
the `player_data_scraper.py` file.

## Data Transforms

The file `dataprep.py` will create an object that will merge the top, meta, and weekly
data together for use in modeling. Providing file paths to each of the datasets
collected above will process the data for modeling.

```
import dataprep as dp
meta_data_location = 'meta_filepath'
top_data_location = 'top_filepath'
weekly_data_location = 'weekly_filepath'

dataprepped = dp.Dataprep(meta_data_location, top_data_location, weekly_data_location)
```

If you want to use data from the first 5 rounds of the season in your modeling, you can run the following script:

```
X_train, X_test, y_train, y_test = dataprepped.get_data_for_modeling(5)
```

For exploring the features and targets I've chosen for modeling, you can run the following
script:

```
features, targets = dataprepped.merge_data()
```

## Modeling and Cross Validation

After looking at a Random Forest as a baseline, I used [PyTorch](https://pytorch.org/) to
build neural networks that had 1, 2, and 3, linear layers, with ReLU activation
layers in between. With 66 dimensions in and 25 dimensions out, the network had
the following layers:

  * First layer with 128 hidden dimensions
  * Second layer with 48 hidden dimensions
  * Third layer with 32 hidden dimensions

To prevent leakage, the training set uses weeks from the beginning of the season,
and the test set uses weeks from later in the season. For example, for week 7, the training
set used data from weeks 1 through 4, and data from weeks 5 and 6 for the test set. MSE
on the output vector is used for minimizing the model error.

Every 3-4 weeks, as data accumulates, models are retrained and the model with the
lowest training error is used for predictions over the upcoming weeks. The following
list tells which models are used for which week.

  * For week 1, a random forest was used for player score predictions.
  * For weeks 2 through 5, the 3 layer neural network was used for predictions.
  * For week 7, the 2 layers neural network was used for predictions.

## Linear Programming

Linear Programming can be used to choose a team for each week. The [**PuLP**](https://coin-or.github.io/pulp/index.html) library
offers the ability to create a `problem` object, to which constraints can be added
using the `+=` python syntax, and then a final objective that asks to find the maximum
or minimum for the problem.

Each week, the `team_selection.py` file can be run and will provide the optimal starters
and subs given the score predictions for each player that week, the constraint of the player's
salary, and finally the league rules about positions and teams. Having links to the three
respective files for `top`, `meta`, and `season` data, along with the the model used for
predictions, will allow the file to run properly. Dictionaries of all variables - meaning
players as affiliated by their positions and the teams for which they play - are built
and added to the `problem` object in order to be applied to a **PuLP** linear programming
solver to find the optimal player selections.

For the `fastbal` team, I used the team shape make-up that predicted the highest
team total for the week, and then selected those players. I filtered only players
who have played at least 1 minute during the season, to avoid bench players being selected
when they won't have the chance to earn points. The [standings for the 2020 season](https://github.com/rsherer/fastbal/blob/master/2020_season_standings.md) update the three teams in the league:

  * fastball FC, managed by the fastbal optimizer
  * Zidane's Forehead, managed by Robert Sherer
  * seagullane, managed by the MLS Fantasy Soccer randomizer

The result each week looks like the following team:

![fastbal team from week 3](img/fastbal_team_week3.png)

## Acknowledgments

I leaned heavily on a [blog post](https://medium.com/ml-everything/using-python-and-linear-programming-to-optimize-fantasy-football-picks-dc9d1229db81) by [Branko Blagojevic](https://github.com/breeko) and the [Blending Problem](https://coin-or.github.io/pulp/CaseStudies/a_blending_problem.html) case study in the [PuLP Library](https://coin-or.github.io/pulp/index.html) to
build the solver for the optimization portion of the project. Thanks also to
[Matt Drury](https://github.com/madrury) for pointing me in the direction of using
linear programming to find the optimal teams given the constraints of the MLS Fantasy Soccer game.