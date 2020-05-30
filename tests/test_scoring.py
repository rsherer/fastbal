import numpy as np
import unittest
import src.scoring as scoring

class ScoringTest(unittest.TestCase):
    def test_minutes(self):
        assert scoring.calculate_minutes_points(65) == 2, scoring.calculate_minutes_points(65)
        assert scoring.calculate_minutes_points(57) == 1, scoring.calculate_minutes_points(57)
        assert scoring.calculate_minutes_points(0) == 0, scoring.calculate_minutes_points(0)

    def test_goals_scored(self):
        assert scoring.calculate_goals_scored_points(2, 'G') == 12