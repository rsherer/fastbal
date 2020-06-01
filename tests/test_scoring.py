import numpy as np
import unittest
from src import scoring as sc

class scTest(unittest.TestCase):
    def test_minutes(self):
        assert sc.points_for_minutes_played(65) == 2, sc.points_for_minutes_played(65)
        assert sc.points_for_minutes_played(57) == 1, sc.points_for_minutes_played(57)
        assert sc.points_for_minutes_played(0) == 0, sc.points_for_minutes_played(0)

    def test_goals_scored(self):
        assert sc.points_for_goals_scored(2, 'G') == 12
        assert sc.points_for_goals_scored(0, 'G') == 0
        assert sc.points_for_goals_scored(0, 'D') == 0
        assert sc.points_for_goals_scored(1, 'D') == 6
        assert sc.points_for_goals_scored(0, 'M') == 0
        assert sc.points_for_goals_scored(1, 'M') == 5
        assert sc.points_for_goals_scored(2, 'M') == 10
        assert sc.points_for_goals_scored(0, 'F') == 0
        assert sc.points_for_goals_scored(1, 'F') == 5
        assert sc.points_for_goals_scored(2, 'F') == 10
        assert sc.points_for_goals_scored(3, 'F') == 15

    def test_assists(self):
        assert sc.points_for_assists(0) == 0
        assert sc.points_for_assists(1) == 3
        assert sc.points_for_assists(2) == 6