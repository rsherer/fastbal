import numpy as np
import unittest
from src import scoring as sc

class TestScoring(unittest.TestCase):
    def test_minutes(self):
        self.assertEqual(sc.points_for_minutes_played(65), 2)
        self.assertEqual(sc.points_for_minutes_played(57), 1)
        self.assertEqual(sc.points_for_minutes_played(0), 0)

    def test_goals_scored(self):
        self.assertEqual(sc.points_for_goals_scored(2, 'G'), 12)
        self.assertEqual(sc.points_for_goals_scored(0, 'G'), 0)
        self.assertEqual(sc.points_for_goals_scored(0, 'D'), 0)
        self.assertEqual(sc.points_for_goals_scored(1, 'D'), 6)
        self.assertEqual(sc.points_for_goals_scored(0, 'M'), 0)
        self.assertEqual(sc.points_for_goals_scored(1, 'M'), 5)
        self.assertEqual(sc.points_for_goals_scored(2, 'M'), 10)
        self.assertEqual(sc.points_for_goals_scored(0, 'F'), 0)
        self.assertEqual(sc.points_for_goals_scored(1, 'F'), 5)
        self.assertEqual(sc.points_for_goals_scored(2, 'F'), 10)
        self.assertEqual(sc.points_for_goals_scored(3, 'F'), 15)

    def test_assists(self):
        self.assertEqual(sc.points_for_assists(0), 0)
        self.assertEqual(sc.points_for_assists(1), 3)
        self.assertEqual(sc.points_for_assists(2), 6)

    def test_clean_sheet(self):
        self.assertEqual(sc.points_for_clean_sheet(0, 'G'), 0)
        self.assertEqual(sc.points_for_clean_sheet(1, 'G'), 5)
        self.assertEqual(sc.points_for_clean_sheet(0, 'D'), 0)
        self.assertEqual(sc.points_for_clean_sheet(1, 'D'), 5)
        self.assertEqual(sc.points_for_clean_sheet(0, 'M'), 0)
        self.assertEqual(sc.points_for_clean_sheet(1, 'M'), 1)
        self.assertEqual(sc.points_for_clean_sheet(0, 'F'), 0)
        self.assertEqual(sc.points_for_clean_sheet(1, 'F'), 0)
        self.assertEqual(sc.points_for_clean_sheet(0, 'D'), 0)
        self.assertEqual(sc.points_for_clean_sheet(2, 'D'), 0)

    def test_penalty_saves(self):
        self.assertEqual(sc.points_for_penalty_save(0), 0)
        self.assertEqual(sc.points_for_penalty_save(1), 5)
        self.assertEqual(sc.points_for_penalty_save(2), 10)

    def test_penalty_earned(self):
        self.assertEqual(sc.points_for_penalty_earned(0), 0)
        self.assertEqual(sc.points_for_penalty_earned(1), 2)
        self.assertEqual(sc.points_for_penalty_earned(3), 6)

    def test_penalty_missed(self):
        self.assertEqual(sc.points_for_penalty_missed(0), 0)
        self.assertEqual(sc.points_for_penalty_missed(1), -2)
        self.assertEqual(sc.points_for_penalty_missed(4), -8)