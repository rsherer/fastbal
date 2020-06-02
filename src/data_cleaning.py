''' functions used for cleaning data that has been scraped from mlssoccer.com
'''
from typing import List

def remove_negative_scores(stats: List[str]) -> List[str]:
    '''Check row of game summary data for a hyphen to indicate a negative
    score, and then update the row for the negative score for the game, and
    correct the length of the row to match the rest of the table.

    Created specifically used for cleaning up the data from top_stats, but
    should be explored to see if it can be repurposed.
    '''
    cols = ['GAMES PLAYED', 'AVG FANTASY PTS', 'TOTAL FANTASY PTS',
            'LAST WK FANTASY PTS', '3 WK AVG', '5 WK AVG', 'HIGH SCORE',
            'LOW SCORE', 'OWNED BY', '$/POINT', 'RD 2 RANK', 'SEASON RANK']

    for i, stat in enumerate(stats):
        if stats[i] == '-' and stats[i + 1] not in cols:
            stats[i + 1] = '-' + stats[i + 1]
            stats[i:] = stats[(i + 1):]
    return stats


def concat_salary_per_point(stats: List[str]) -> List[str]:
    '''Used for top stats data, to clean up possibility of raw scraped text
    having a cost per point bisected by a ','. The function will look to see
    if the cost per point field is following by more than 1 field, concat the
    two and remove the trailing field.
    '''
    for i, stat in enumerate(stats):
        if stats[i] == '$/POINT' and stats[i + 2][:2] != 'RD':
            stats[i + 1] = stats[i + 1] + stats[i + 2]
            stats.pop(i + 2)
    return stats
    