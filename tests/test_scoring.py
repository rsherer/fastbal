import numpy as np
import unittest
from src import scoring_functions as sc

class TestScoring(unittest.TestCase):
    def test_minutes(self):
        self.assertEqual(sc.minutes_played(65), 2)
        self.assertEqual(sc.minutes_played(57), 1)
        self.assertEqual(sc.minutes_played(0), 0)

    def test_goals_scored(self):
        self.assertEqual(sc.goals_scored(2, 'G'), 12)
        self.assertEqual(sc.goals_scored(0, 'G'), 0)
        self.assertEqual(sc.goals_scored(0, 'D'), 0)
        self.assertEqual(sc.goals_scored(1, 'D'), 6)
        self.assertEqual(sc.goals_scored(0, 'M'), 0)
        self.assertEqual(sc.goals_scored(1, 'M'), 5)
        self.assertEqual(sc.goals_scored(2, 'M'), 10)
        self.assertEqual(sc.goals_scored(0, 'F'), 0)
        self.assertEqual(sc.goals_scored(1, 'F'), 5)
        self.assertEqual(sc.goals_scored(2, 'F'), 10)
        self.assertEqual(sc.goals_scored(3, 'F'), 15)

    def test_assists(self):
        self.assertEqual(sc.assists(0), 0)
        self.assertEqual(sc.assists(1), 3)
        self.assertEqual(sc.assists(2), 6)

    def test_clean_sheet(self):
        self.assertEqual(sc.clean_sheet(0, 'G'), 0)
        self.assertEqual(sc.clean_sheet(1, 'G'), 5)
        self.assertEqual(sc.clean_sheet(0, 'D'), 0)
        self.assertEqual(sc.clean_sheet(1, 'D'), 5)
        self.assertEqual(sc.clean_sheet(0, 'M'), 0)
        self.assertEqual(sc.clean_sheet(1, 'M'), 1)
        self.assertEqual(sc.clean_sheet(0, 'F'), 0)
        self.assertEqual(sc.clean_sheet(1, 'F'), 0)
        self.assertEqual(sc.clean_sheet(0, 'D'), 0)
        self.assertEqual(sc.clean_sheet(2, 'D'), 0)
        with self.assertRaises(ValueError):
            sc.clean_sheet(3, 'u')
        with self.assertRaises(ValueError):
            sc.clean_sheet(3, '')

    def test_penalty_saves(self):
        self.assertEqual(sc.penalty_save(0), 0)
        self.assertEqual(sc.penalty_save(1), 5)
        self.assertEqual(sc.penalty_save(2), 10)

    def test_penalty_earned(self):
        self.assertEqual(sc.penalty_earned(0), 0)
        self.assertEqual(sc.penalty_earned(1), 2)
        self.assertEqual(sc.penalty_earned(3), 6)

    def test_penalty_missed(self):
        self.assertEqual(sc.penalty_missed(0), 0)
        self.assertEqual(sc.penalty_missed(1), -2)
        self.assertEqual(sc.penalty_missed(4), -8)

    def test_goal_against(self):
        self.assertEqual(sc.goal_against(0, 'D'), 0)
        self.assertEqual(sc.goal_against(0, 'G'), 0)
        self.assertEqual(sc.goal_against(0, 'M'), 0)
        self.assertEqual(sc.goal_against(0, 'F'), 0)
        self.assertEqual(sc.goal_against(1, 'D'), 0)
        self.assertEqual(sc.goal_against(1, 'G'), 0)
        self.assertEqual(sc.goal_against(1, 'M'), 0)
        self.assertEqual(sc.goal_against(1, 'F'), 0)
        self.assertEqual(sc.goal_against(2, 'D'), -1)
        self.assertEqual(sc.goal_against(2, 'G'), -1)
        self.assertEqual(sc.goal_against(2, 'M'), 0)
        self.assertEqual(sc.goal_against(2, 'F'), 0)
        self.assertEqual(sc.goal_against(3, 'D'), -1)
        self.assertEqual(sc.goal_against(3, 'G'), -1)
        self.assertEqual(sc.goal_against(3, 'M'), 0)
        self.assertEqual(sc.goal_against(3, 'F'), 0)
        self.assertEqual(sc.goal_against(4, 'D'), -2)
        self.assertEqual(sc.goal_against(4, 'G'), -2)
        self.assertEqual(sc.goal_against(5, 'D'), -2)
        self.assertEqual(sc.goal_against(6, 'D'), -3)
        with self.assertRaises(ValueError):
            sc.goal_against(2, 'U')
        with self.assertRaises(ValueError):
            sc.goal_against(3, '')

    def test_saves(self):
        self.assertEqual(sc.saves(0), 0)
        self.assertEqual(sc.saves(1), 0)
        self.assertEqual(sc.saves(3), 1)
        self.assertEqual(sc.saves(4), 1)
        self.assertEqual(sc.saves(6), 2)

    def test_yellows(self):
        self.assertEqual(sc.yellow_cards(0), 0)
        self.assertEqual(sc.yellow_cards(1), -1)
        self.assertEqual(sc.yellow_cards(2), -2)

    def test_reds(self):
        self.assertEqual(sc.red_cards(0), 0)
        self.assertEqual(sc.red_cards(1), -3)

    def test_own_goals(self):
        self.assertEqual(sc.own_goal(0), 0)
        self.assertEqual(sc.own_goal(1), -2)
        self.assertEqual(sc.own_goal(3), -6)

    def test_tackles(self):
        self.assertEqual(sc.tackles(0), 0)
        self.assertEqual(sc.tackles(1), 0)
        self.assertEqual(sc.tackles(3), 0)
        self.assertEqual(sc.tackles(4), 1)
        self.assertEqual(sc.tackles(7), 1)
        self.assertEqual(sc.tackles(8), 2)
        self.assertEqual(sc.tackles(11), 2)
        self.assertEqual(sc.tackles(12), 3)

    def test_passes(self):
        self.assertEqual(sc.passes(0), 0)
        self.assertEqual(sc.passes(20), 0)
        self.assertEqual(sc.passes(35), 1)
        self.assertEqual(sc.passes(55), 1)
        self.assertEqual(sc.passes(70), 2)
        self.assertEqual(sc.passes(75), 2)
        self.assertEqual(sc.passes(110), 3)

    def test_key_passes(self):
        self.assertEqual(sc.key_passes(0), 0)
        self.assertEqual(sc.key_passes(1), 0)
        self.assertEqual(sc.key_passes(2), 0)
        self.assertEqual(sc.key_passes(3), 1)
        self.assertEqual(sc.key_passes(4), 1)
        self.assertEqual(sc.key_passes(6), 2)
        self.assertEqual(sc.key_passes(8), 2)
        self.assertEqual(sc.key_passes(9), 3)

    def test_crosses(self):
        self.assertEqual(sc.crosses(0), 0)
        self.assertEqual(sc.crosses(1), 0)
        self.assertEqual(sc.crosses(2), 0)
        self.assertEqual(sc.crosses(3), 1)
        self.assertEqual(sc.crosses(4), 1)
        self.assertEqual(sc.crosses(6), 2)
        self.assertEqual(sc.crosses(8), 2)
        self.assertEqual(sc.crosses(9), 3)

    def test_big_chance(self):
        self.assertEqual(sc.big_chance(0), 0)
        self.assertEqual(sc.big_chance(1), 1)
        self.assertEqual(sc.big_chance(2), 2)
        self.assertEqual(sc.big_chance(4), 4)
        self.assertEqual(sc.big_chance(5), 5)

    def test_clearances(self):
        self.assertEqual(sc.clearances(0), 0)
        self.assertEqual(sc.clearances(1), 0)
        self.assertEqual(sc.clearances(4), 1)
        self.assertEqual(sc.clearances(5), 1)
        self.assertEqual(sc.clearances(12), 3)

    def test_blocks(self):
        self.assertEqual(sc.blocks(0), 0)
        self.assertEqual(sc.blocks(1), 0)
        self.assertEqual(sc.blocks(2), 1)
        self.assertEqual(sc.blocks(3), 1)
        self.assertEqual(sc.blocks(4), 2)
        self.assertEqual(sc.blocks(8), 4)

    def test_interceptions(self):
        self.assertEqual(sc.interceptions(0), 0)
        self.assertEqual(sc.interceptions(1), 0)
        self.assertEqual(sc.interceptions(2), 0)
        self.assertEqual(sc.interceptions(3), 0)
        self.assertEqual(sc.interceptions(4), 1)
        self.assertEqual(sc.interceptions(7), 1)
        self.assertEqual(sc.interceptions(8), 2)
        self.assertEqual(sc.interceptions(12), 3)

    def test_recovered_balls(self):
        self.assertEqual(sc.recovered_balls(0), 0)
        self.assertEqual(sc.recovered_balls(5), 0)
        self.assertEqual(sc.recovered_balls(6), 1)
        self.assertEqual(sc.recovered_balls(7), 1)
        self.assertEqual(sc.recovered_balls(12), 2)

    def test_error_leading_to_goal(self):
        self.assertEqual(sc.error_leading_to_goal(0), 0)
        self.assertEqual(sc.error_leading_to_goal(1), -1)
        self.assertEqual(sc.error_leading_to_goal(2), -2)
        self.assertEqual(sc.error_leading_to_goal(3), -3)
        self.assertNotEqual(sc.error_leading_to_goal(4), 2)

    def test_own_goal_assist(self):
        self.assertEqual(sc.own_goal_assist(0), 0)
        self.assertEqual(sc.own_goal_assist(1), 1)
        self.assertEqual(sc.own_goal_assist(2), 2)
        self.assertEqual(sc.own_goal_assist(3), 3)
        self.assertNotEqual(sc.own_goal_assist(2), 3)
    
    def test_shots(self):
        self.assertEqual(sc.shots(0), 0)
        self.assertEqual(sc.shots(1), 0)
        self.assertEqual(sc.shots(3), 0)
        self.assertEqual(sc.shots(4), 1)
        self.assertEqual(sc.shots(6), 1)
        self.assertEqual(sc.shots(8), 2)
        self.assertEqual(sc.shots(9), 2)
        self.assertNotEqual(sc.shots(3), 2)

    def test_was_fouled(self):
        self.assertEqual(sc.was_fouled(0), 0)
        self.assertEqual(sc.was_fouled(1), 0)
        self.assertEqual(sc.was_fouled(3), 0)
        self.assertEqual(sc.was_fouled(4), 1)
        self.assertEqual(sc.was_fouled(6), 1)
        self.assertEqual(sc.was_fouled(8), 2)
        self.assertEqual(sc.was_fouled(9), 2)
        self.assertNotEqual(sc.was_fouled(3), 2)