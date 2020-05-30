import numpy as numpy

season_stats_columns = ['ID', 'NAME', 'TEAM', 'RD', 'HOME_AWAY', 'OPPONENT',
                        'PTS', 'MIN', 'GF', 'A', 'CS', 'PS', 'PE', 'PM', 'GA', 
                        'SV', 'Y', 'R', 'OG', 'T', 'P', 'KP', 'CRS', 'BC', 
                        'CL', 'BLK', 'INT', 'BR', 'ELG', 'OGA', 'SH', 'WF']

### to do: create functions for each column that is used to total
### game by game fantasy points.

def calculate_minutes_points(minutes: int) -> int:
    '''Calculate the number of fantasy points for the 'MIN' column for each
    player's games.
    '''
    if minutes >= 60:
        return 2
    elif minutes > 0:
        return 1
    else:
        return 0

def calculate_goals_scored_points(goals: int, position: str) -> int:
    '''Calculate fantasy points for goals scored. 6 points for a goalkeeper
    or a defender, 5 points for a midfielder or forward.
    '''
    assert position in ['G', 'D', 'M', 'F'], 'Not a valid position'
    if position in ['G', 'D']:
        return 6 * goals
    if position in ['M', 'F']:
        return 5 * goals
