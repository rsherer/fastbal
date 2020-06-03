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
    if position not in ['G', 'D', 'M', 'F']:
        raise ValueError(
    f'{position} is not valid. Positions can only be: "G", "D", "M", or "F"'
    )
    if position in ['G', 'D']:
        return goals * 6
    else:
        return goals * 5

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
    if position not in ['G', 'D', 'M', 'F']:
        raise ValueError(
    f'{position} is not valid. Positions can only be: "G", "D", "M", or "F"'
    )
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
    penalty save.
    '''
    return saves * 5

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

def goal_against(ga: int, position: str) -> int:
    '''Calculate fantasy points for 'GA', goals scored against the player's
    team. For goalkeepers and defenders, a negative point is earned for every
    two goals against.
    '''
    if position not in ['G', 'D', 'M', 'F']:
        raise ValueError(
    f'{position} is not valid. Positions can only be: "G", "D", "M", or "F"'
    )
    if position in ['G', 'D'] and ga > 1:
        return (ga // 2) * -1
    else:
        return 0

def saves(saves: int) -> int:
    '''Calculate fantasy points for 'S', saves made during the match. For 
    goalkeepers, primarily. One point is earned for every three saves.
    '''
    return saves // 3

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

def own_goal(og: int) -> int:
    '''Calculate fantasy points earned for 'OG', own goals in a match. Two 
    negative points are earned for a red card.
    '''
    return og * -2

def tackles(t: int) -> int:
    '''Calculate fantasy points earned for 'T', tackles in a match. One point
    is earned for every four tackles in a match.
    '''
    return t // 4

def passes(passes: int) -> int:
    '''Calculate fantasy points earned for 'P', passes in a match. A fantasy
    point is awarded for every 35 passes, AND if the pass success rate is 
    above 85%.
    '''
    # to do: not sure if there is any way to know if the pass success rate
    # is above 85%, other than points awarded in this category. Will need
    # to update this code for the additional condition of successful passes.
    return passes // 35
 
def key_passes(kp: int) -> int:
    '''Calculate fantasy points earned for 'KP', key passes in a match. A key
    pass is a pass theat leads to a shot on goal. 1 point is earned for
    every 3 key passes.
    '''
    return kp // 3

def crosses(crosses: int) -> int:
    '''Calculate fantasy points earned for 'CRS', crosses in a match. A cross
    is defined where the ball is played to their own player in the penalty
    area. 1 point is earned for every 3 crosses.
    '''
    return crosses // 3

def big_chance(bc: int) -> int:
    '''Calculate fantasy points earned for 'BC', big changes created. A big
    change created is one where the analyst/scorekeeper determines the player
    should score. 1 point is earned for each big chance created in a match.
    '''
    return bc

def clearances(c: int) -> int:
    '''Calculate fantasy points earned for 'CL', clearances. 1 point is 
    earned for every 4 clearances in a match.
    '''
    return c // 4

def blocks(blk: int) -> int:
    '''Calculate fantasy points earned for 'BLK', blocks. 1 point is earned
    for every 2 blocks in a match.
    '''
    return blk // 2

def interceptions(interceptions: int) -> int:
    '''Calculate fantasy points earned for 'INT', interceptions in a match.
    1 point is earned for every 4 interceptions.
    '''
    return interceptions // 4

def recovered_balls(rb: int) -> int:
    '''Calculate fantasy points earned fo 'BR', balls recovered in a match. 1 
    point is earned for every 6 recovered balls.
    '''
    return rb // 6

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

def shots(shots: int) -> int:
    '''Calculate fantasy points earned fo 'SH', shots in a match. 1 
    point is earned for every 4 shots.
    '''
    return shots // 4

def was_fouled(wf: int) -> int:
    '''Calculate fantasy points earned fo 'WF', fouls received in a match. 1 
    point is earned for every 4 fouls received.
    '''
    return wf // 4