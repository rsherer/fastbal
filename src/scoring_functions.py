'''Functions for converting player game statistics into fantasy points.
'''
from typing import NamedTuple, Any
import numpy as np

# keeping for now, but this global variable likely isn't necessary
SEASON_STATS_COLUMNS = ['ID', 'NAME', 'TEAM', 'RD', 'HOME_AWAY', 'OPPONENT',
                        'PTS', 'MIN', 'GF', 'A', 'CS', 'PS', 'PE', 'PM', 'GA',
                        'SV', 'Y', 'R', 'OG', 'T', 'P', 'KP', 'CRS', 'BC',
                        'CL', 'BLK', 'INT', 'BR', 'ELG', 'OGA', 'SH', 'WF']

class PlayerData(NamedTuple):
    '''NamedTuple which has as attributes match stats for a player for a
    specific game.
    '''
    minutes: Any
    goals_for: Any
    assists_earned: Any
    shutout: Any
    pen_save: Any
    pen_earned: Any
    pen_missed: Any
    goals_against: Any
    saves_made: Any
    yellows: Any
    reds: Any
    own_goals: Any
    tackles_made: Any
    passes_completed: Any
    key_passes_made: Any
    crosses_made: Any
    big_chances_created: Any
    clearances_made: Any
    blocks_made: Any
    interceptions_won: Any
    balls_recovered: Any
    error_leading_goal: Any
    own_goal_assists: Any
    shots_taken: Any
    fouls_suffered: Any

class GoalieOrDefender(PlayerData):
    '''GoalieOrDefender is the base class for player statse earned during a
    match, and uses those stats to calculate the player's fantasy score for
    said match.
    '''
    def minutes_played(self) -> int:
        '''Calculate the number of fantasy points for the 'MIN' column for each
        player's games.
        '''
        if self.minutes >= 60:
            return 2
        if self.minutes > 0:
            return 1
        return 0

    def goals_scored(self) -> int:
        '''Calculate fantasy points for 'GF' column which is goals scored.
        6 points for each goal.
        '''
        return self.goals_for * 6

    def assists(self) -> int:
        '''Calculate fantasy points for 'A', which is assists in a match. Each
        assist or secondary assist during a match is 3 points for the player.
        '''
        return self.assists_earned * 3

    def clean_sheet(self) -> int:
        '''Calculate fantasy points for 'CS', which is for a clean sheet, meaning
        the defense gives up zero goals. Five points for each clean sheet.
        '''
        if self.minutes >= 60 and self.shutout != 0:
            return 5
        return 0

    def penalty_save(self) -> int:
        '''Calculate fantasy points for 'PS', penalties saved. Generally
        attributed to goalies, the column exists for all players. 5 points per
        penalty save.
        '''
        return self.pen_save * 5

    def penalty_earned(self) -> int:
        '''Calculate fantasy points for 'PE', penalties earned. For players
        fouled in the penalty box, earning a penalty change for their team.
        Two points for each penalty earned.
        '''
        return self.pen_earned * 2

    def penalty_missed(self) -> int:
        '''Calculate fantasy points for 'PM', penalties missed. For players who
        attempt a penalty kick, and miss for whatever reason. Negative two points
        are earned for each penalty miss.
        '''
        return self.pen_missed * -2

    def goal_against(self) -> int:
        '''The is an experimental function where position is not considered.

        Calculate fantasy points for 'GA', goals scored against the player's
        team. A negative point is earned for every two goals against.
        '''
        if self.goals_against >= 2:
            return (self.goals_against // 2) * -1
        return 0

    def saves(self) -> int:
        '''Calculate fantasy points for 'S', saves made during the match. For
        goalkeepers, primarily. One point is earned for every three saves.
        '''
        return self.saves_made // 3

    def yellow_cards(self) -> int:
        '''Calculate fantasy points for 'Y', yellows cards received during a
        match. One negative point is earned for each yellow card.
        '''
        return self.yellows * -1

    def red_cards(self) -> int:
        '''Calculate fantasy points for 'R', red cards received during a match.
        Three negative points are earned for a red card.
        '''
        return self.reds * -3

    def own_goal(self) -> int:
        '''Calculate fantasy points earned for 'OG', own goals in a match. Two
        negative points are earned for a red card.
        '''
        return self.own_goals * -2

    def tackles(self) -> int:
        '''Calculate fantasy points earned for 'T', tackles in a match. One point
        is earned for every four tackles in a match.
        '''
        return self.tackles_made // 4

    def passes(self) -> int:
        '''Calculate fantasy points earned for 'P', passes in a match. A fantasy
        point is awarded for every 35 passes, AND if the pass success rate is
        above 85%.
        '''
        # to do: not sure if there is any way to know if the pass success rate
        # is above 85%, other than points awarded in this category. Will need
        # to update this code for the additional condition of successful passes.
        return self.passes_completed // 35

    def key_passes(self) -> int:
        '''Calculate fantasy points earned for 'KP', key passes in a match. A key
        pass is a pass theat leads to a shot on goal. 1 point is earned for
        every 3 key passes.
        '''
        return self.key_passes_made // 3

    def crosses(self) -> int:
        '''Calculate fantasy points earned for 'CRS', crosses in a match. A cross
        is defined where the ball is played to their own player in the penalty
        area. 1 point is earned for every 3 crosses.
        '''
        return self.crosses_made // 3

    def big_chance(self) -> int:
        '''Calculate fantasy points earned for 'BC', big changes created. A big
        change created is one where the analyst/scorekeeper determines the player
        should score. 1 point is earned for each big chance created in a match.
        '''
        return self.big_chances_created

    def clearances(self) -> int:
        '''Calculate fantasy points earned for 'CL', clearances. 1 point is
        earned for every 4 clearances in a match.
        '''
        return self.clearances_made // 4

    def blocks(self) -> int:
        '''Calculate fantasy points earned for 'BLK', blocks. 1 point is earned
        for every 2 blocks in a match.
        '''
        return self.blocks_made // 2

    def interceptions(self) -> int:
        '''Calculate fantasy points earned for 'INT', interceptions in a match.
        1 point is earned for every 4 interceptions.
        '''
        return self.interceptions_won // 4

    def recovered_balls(self) -> int:
        '''Calculate fantasy points earned fo 'BR', balls recovered in a match. 1
        point is earned for every 6 recovered balls.
        '''
        return self.balls_recovered // 6

    def error_leading_to_goal(self) -> int:
        '''Calculate fantasy points earned fo 'ELG', erros leading to a goal in
        a match. Negative 1 point is earned for every error leading to a goal.
        '''
        return -self.error_leading_goal

    def own_goal_assist(self) -> int:
        '''Calculate fantasy points earned fo 'OGA', own goal assists in a match.
        1 point is earned for every own goal assist.
        '''
        return self.own_goal_assists

    def shots(self) -> int:
        '''Calculate fantasy points earned fo 'SH', shots in a match. 1
        point is earned for every 4 shots.
        '''
        return self.shots_taken // 4

    def was_fouled(self) -> int:
        '''Calculate fantasy points earned fo 'WF', fouls received in a match. 1
        point is earned for every 4 fouls received.
        '''
        return self.fouls_suffered // 4

    def score(self):
        '''Calculate a player's fantasy score using the stats from the game.
        '''
        return np.sum([
            self.minutes_played(),
            self.goals_scored(),
            self.assists(),
            self.clean_sheet(),
            self.penalty_save(),
            self.penalty_earned(),
            self.penalty_missed(),
            self.goal_against(),
            self.saves(),
            self.yellow_cards(),
            self.red_cards(),
            self.own_goal(),
            self.tackles(),
            self.passes(),
            self.key_passes(),
            self.crosses(),
            self.big_chance(),
            self.clearances(),
            self.blocks(),
            self.interceptions(),
            self.recovered_balls(),
            self.error_leading_to_goal(),
            self.own_goal_assist(),
            self.shots(),
            self.was_fouled()])

class Midfielder(GoalieOrDefender):
    '''Midfielder class inherits from base class GoalieOrDefender, with
    methods overriding for Midfielder-specific scoring.
    '''
    def goals_scored(self) -> int:
        '''Calculate fantasy points for 'GF' column which is goals scored.
        Midfielders score 5 points for each goal.
        '''
        return self.goals_for * 5

    def clean_sheet(self) -> int:
        '''Calculate fantasy points for 'CS', which is for a clean sheet,
        meaning the defense gives up zero goals. Midfielders get 1 point for
        a clean sheet.
        '''
        if self.minutes >= 60 and self.shutout != 0:
            return 1
        return 0

    def goal_against(self) -> int:
        '''Calculate fantasy points for 'GA', goals scored against the
        player's team. Midfielders are not penalized for goals against.
        '''
        return 0

class Forward(Midfielder):
    '''Forward class inherits from Midfielder class, with clean_sheet method
    writen to always return zero.
    '''
    def clean_sheet(self):
        return 0
