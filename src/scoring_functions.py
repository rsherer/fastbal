'''Functions for converting player game statistics into fantasy points.
'''
from typing import NamedTuple
import numpy as np


SEASON_STATS_COLUMNS = ['ID', 'NAME', 'TEAM', 'RD', 'HOME_AWAY', 'OPPONENT',
                        'PTS', 'MIN', 'GF', 'A', 'CS', 'PS', 'PE', 'PM', 'GA',
                        'SV', 'Y', 'R', 'OG', 'T', 'P', 'KP', 'CRS', 'BC',
                        'CL', 'BLK', 'INT', 'BR', 'ELG', 'OGA', 'SH', 'WF']


def minutes_played(minutes: int) -> int:
    '''Calculate the number of fantasy points for the 'MIN' column for each
    player's games.
    '''
    if minutes >= 60:
        return 2
    if minutes > 0:
        return 1
    return 0

def goals_scored_by_pos(goals: int, position: str) -> int:
    '''Calculate fantasy points for 'GF' column which is goals scored.
    6 points for a goalkeeper or a defender, 5 points for a midfielder
    or forward.
    '''
    if position not in ['G', 'D', 'M', 'F']:
        raise ValueError(
            f'{position} is not valid. Positions can only be: \
                "G", "D", "M", or "F"'
        )
    if position in ['G', 'D']:
        return goals * 6
    return goals * 5

def goals_scored(goals: int) -> int:
    '''This is a experimental function which does not consider position.

    Calculate fantasy points for 'GF' column which is goals scored.
    6 points for each goal.
    '''
    return goals * 5

def assists(assts: int) -> int:
    '''Calculate fantasy points for 'A', which is assists in a match. Each
    assist or secondary assist during a match is 3 points for the player.
    '''
    return assts * 3

def clean_sheet_by_pos(shutout: int, position: str) -> int:
    '''Calculate fantasy points for 'CS', which is for a clean sheet, meaning
    the defense gives up zero goals. A goalkeeper ('G') or a defender ('D')
    will receive 6 points, a midfielder ('M') will receive 1 point.
    '''
    if position not in ['G', 'D', 'M', 'F']:
        raise ValueError(
            f'{position} is not valid. Positions can only be: \
                "G", "D", "M", or "F"'
        )
    if shutout != 1:
        return 0
    if position in ['G', 'D']:
        return 5
    if position == 'M':
        return 1
    return 0

def clean_sheet(shutout: int) -> int:
    '''This is a experimental function which does not consider position.

    Calculate fantasy points for 'CS', which is for a clean sheet, meaning
    the defense gives up zero goals. Five points for each clean sheet.
    '''
    if shutout != 1:
        return 0
    return 5

def penalty_save(pen_saves: int) -> int:
    '''Calculate fantasy points for 'PS', penalties saved. Generally
    attributed to goalies, the column exists for all players. 5 points per
    penalty save.
    '''
    return pen_saves * 5

def penalty_earned(earned: int) -> int:
    '''Calculate fantasy points for 'PE', penalties earned. For players
    fouled in the penalty box, earning a penalty change for their team.
    Two points for each penalty earned.
    '''
    return earned * 2

def penalty_missed(missed: int) -> int:
    '''Calculate fantasy points for 'PM', penalties missed. For players who
    attempt a penalty kick, and miss for whatever reason. Negative two points
    are earned for each penalty miss.
    '''
    return missed * -2

def goal_against_by_pos(against: int, position: str) -> int:
    '''Calculate fantasy points for 'GA', goals scored against the player's
    team. For goalkeepers and defenders, a negative point is earned for every
    two goals against.
    '''
    if position not in ['G', 'D', 'M', 'F']:
        raise ValueError(
            f'{position} is not valid. Positions can only be: \
                "G", "D", "M", or "F"'
        )
    if position in ['G', 'D'] and against > 1:
        return (against // 2) * -1
    return 0

def goal_against(against: int) -> int:
    '''The is an experimental function where position is not considered.

    Calculate fantasy points for 'GA', goals scored against the player's
    team. A negative point is earned for every two goals against.
    '''
    if against >= 2:
        return (against // 2) * -1
    return 0

def saves(shots_saved: int) -> int:
    '''Calculate fantasy points for 'S', saves made during the match. For
    goalkeepers, primarily. One point is earned for every three saves.
    '''
    return shots_saved // 3

def yellow_cards(yellows: int) -> int:
    '''Calculate fantasy points for 'Y', yellows cards received during a
    match. One negative point is earned for each yellow card.
    '''
    return yellows * -1

def red_cards(reds: int) -> int:
    '''Calculate fantasy points for 'R', red cards received during a match.
    Three negative points are earned for a red card.
    '''
    return reds * -3

def own_goal(own_goals: int) -> int:
    '''Calculate fantasy points earned for 'OG', own goals in a match. Two
    negative points are earned for a red card.
    '''
    return own_goals * -2

def tackles(tackles_won: int) -> int:
    '''Calculate fantasy points earned for 'T', tackles in a match. One point
    is earned for every four tackles in a match.
    '''
    return tackles_won // 4

def passes(passes_completed: int) -> int:
    '''Calculate fantasy points earned for 'P', passes in a match. A fantasy
    point is awarded for every 35 passes, AND if the pass success rate is
    above 85%.
    '''
    # to do: not sure if there is any way to know if the pass success rate
    # is above 85%, other than points awarded in this category. Will need
    # to update this code for the additional condition of successful passes.
    return passes_completed // 35

def key_passes(kp_made: int) -> int:
    '''Calculate fantasy points earned for 'KP', key passes in a match. A key
    pass is a pass theat leads to a shot on goal. 1 point is earned for
    every 3 key passes.
    '''
    return kp_made // 3

def crosses(crosses_made: int) -> int:
    '''Calculate fantasy points earned for 'CRS', crosses in a match. A cross
    is defined where the ball is played to their own player in the penalty
    area. 1 point is earned for every 3 crosses.
    '''
    return crosses_made // 3

def big_chance(bc_created: int) -> int:
    '''Calculate fantasy points earned for 'BC', big changes created. A big
    change created is one where the analyst/scorekeeper determines the player
    should score. 1 point is earned for each big chance created in a match.
    '''
    return bc_created

def clearances(clears: int) -> int:
    '''Calculate fantasy points earned for 'CL', clearances. 1 point is
    earned for every 4 clearances in a match.
    '''
    return clears // 4

def blocks(blk: int) -> int:
    '''Calculate fantasy points earned for 'BLK', blocks. 1 point is earned
    for every 2 blocks in a match.
    '''
    return blk // 2

def interceptions(interceptions_made: int) -> int:
    '''Calculate fantasy points earned for 'INT', interceptions in a match.
    1 point is earned for every 4 interceptions.
    '''
    return interceptions_made // 4

def recovered_balls(recoveries: int) -> int:
    '''Calculate fantasy points earned fo 'BR', balls recovered in a match. 1
    point is earned for every 6 recovered balls.
    '''
    return recoveries // 6

def error_leading_to_goal(elg: int) -> int:
    '''Calculate fantasy points earned fo 'ELG', erros leading to a goal in
    a match. Negative 1 point is earned for every error leading to a goal.
    '''
    return -elg

def own_goal_assist(oga: int) -> int:
    '''Calculate fantasy points earned fo 'OGA', own goal assists in a match.
    1 point is earned for every own goal assist.
    '''
    return oga

def shots(shots_taken: int) -> int:
    '''Calculate fantasy points earned fo 'SH', shots in a match. 1
    point is earned for every 4 shots.
    '''
    return shots_taken // 4

def was_fouled(fouls: int) -> int:
    '''Calculate fantasy points earned fo 'WF', fouls received in a match. 1
    point is earned for every 4 fouls received.
    '''
    return fouls // 4

class PlayerData(NamedTuple):
    '''NamedTuple which has as attributes match stats for a player for a
    specific game.
    '''
    minutes: float
    gf: float
    a: float
    cs: float
    ps: float
    pe: float
    pm: float
    ga: float
    sv: float
    y: float
    r: float
    og: float
    t: float
    p: float
    kp: float
    crs: float
    bc: float
    cl: float
    blk: float
    intercept: float
    br: float
    elg: float
    oga: float
    sh: float
    wf: float

class PlayerScores(PlayerData):
    '''PlayerScores takes the stats a player records for a match, and
    uses those stats to calculate the player's fantasy score for the match.
    '''
    def score(self):
        '''Calculate a player's fantasy score using the stats from the game.
        '''
        return (
            minutes_played(self.minutes)
            + goals_scored(self.gf)
            + assists(self.a)
            + clean_sheet(self.cs)
            + penalty_save(self.ps)
            + penalty_earned(self.pe)
            + penalty_missed(self.pm)
            + goal_against(self.ga)
            + saves(self.sv)
            + yellow_cards(self.y)
            + red_cards(self.r)
            + own_goal(self.og)
            + tackles(self.t)
            + passes(self.p)
            + key_passes(self.kp)
            + crosses(self.crs)
            + big_chance(self.bc)
            + clearances(self.cl)
            + blocks(self.blk)
            + interceptions(self.intercept)
            + recovered_balls(self.br)
            + error_leading_to_goal(self.elg)
            + own_goal_assist(self.oga)
            + shots(self.sh)
            + was_fouled(self.wf)
        )

class GoalieOrDefender(PlayerScores):
    def goals_scored(self):
        return self.gf * 6

class Midfielder(PlayerScores):
    def clean_sheet(self):
        if self.cs != 0:
            return 1
        return 0

    def goal_against(self):
        return 0

class Forward(PlayerScores):
    def clean_sheet(self):
        return 0

    def goal_against(self):
        return 0
