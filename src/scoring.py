import numpy as np 

season_stats_columns = ['ID', 'NAME', 'TEAM', 'RD', 'HOME_AWAY', 'OPPONENT',
                        'PTS', 'MIN', 'GF', 'A', 'CS', 'PS', 'PE', 'PM', 'GA', 
                        'SV', 'Y', 'R', 'OG', 'T', 'P', 'KP', 'CRS', 'BC', 
                        'CL', 'BLK', 'INT', 'BR', 'ELG', 'OGA', 'SH', 'WF']

### to do: create functions for each column that is used to total
### game by game fantasy points. Points are calculated from the category 'MIN'
### onward

def minutes_played(minutes: int) -> int:
    '''Calculate the number of fantasy points for the 'MIN' column for each
    player's games.
    '''
    if minutes >= 60:
        return 2
    elif minutes > 0:
        return 1
    else:
        return 0

def goals_scored(goals: int, position: str) -> int:
    '''Calculate fantasy points for 'GF' column which is goals scored. 
    6 points for a goalkeeper or a defender, 5 points for a midfielder 
    or forward.
    '''
    assert position in ['G', 'D', 'M', 'F'], 'Not a valid position'
    if position in ['G', 'D']:
        return goals * 6
    elif position in ['M', 'F']:
        return goals * 5
    else:
        return 0

def assists(assists: int) -> int:
    '''Calculate fantasy points for 'A', which is assists in a match. Each
    assist or secondary assist during a match is 3 points for the player.
    '''
    return assists * 3

def clean_sheet(clean_sheet: int, position: str) -> int:
    '''Calculate fantasy points for 'CS', which is for a clean sheet, meaning
    the defense gives up zero goals. A goalkeeper ('G') or a defender ('D')
    will receive 6 points, a midfielder ('M') will receive 1 point.
    '''
    if clean_sheet != 1:
        return 0
    elif position in ['G', 'D']:
        return 5
    elif position == 'M':
        return 1
    else:
        return 0

def penalty_save(saves: int) -> int:
    '''Calculate fantasy points for 'PS', penalties saved. Generally
    attributed to goalies, the column exists for all players. 5 points per
    penalty save.'''
    if saves > 0:
        return saves * 5
    else:
        return 0

def penalty_earned(earned: int) -> int:
    '''Calculate fantasy points for 'PE', penalties earned. For players
    fouled in the penalty box, earning a penalty change for their team.
    Two points for each penalty earned.
    '''
    if earned > 0:
        return earned * 2
    else:
        return 0

def penalty_missed(missed: int) -> int:
    '''Calculate fantasy points for 'PM', penalties missed. For players who
    attempt a penalty kick, and miss for whatever reason. Negative two points
    are earned for each penalty miss.
    '''
    if missed > 0:
        return missed * -2
    else:
        return 0
