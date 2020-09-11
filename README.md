# fastbal -> FAntasy Soccer Team By ALgorithm
Using machine learning and linear programming to choose an MLS Fantasy soccer team.

## This project includes the following sections:

  * [Data Collection](#data-collection)
  * Data transformation for use in modeling
  * Modeling and cross validation
  * Linear Programming to guide team selection based on model predictions
  * [Acknowledgements](#acknowledgments)


## Data Collection

Training data and target data was collected by scraping data from the [MLS Fantasy Soccer](fantasy.mlssoccer.com) website.

## Data Transforms

## Modeling and Cross Validation

## Linear Programming

## Acknowledgments

I leaned heavily on a [blog post](https://medium.com/ml-everything/using-python-and-linear-programming-to-optimize-fantasy-football-picks-dc9d1229db81) by [Branko Blagojevic](https://github.com/breeko) and the [Blending Problem](https://coin-or.github.io/pulp/CaseStudies/a_blending_problem.html) case study in the [PuLP Library](https://coin-or.github.io/pulp/index.html) to
build the solver for the optimization portion of the project. Thanks also to
[madrury](https://github.com/madrury) for pointing me in the direction of using
linear programming to find the optimal teams given the constraints of the MLS Fantasy Soccer game.