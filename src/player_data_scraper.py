'''Code for the scraper portion of getting stats from the fantasy soccer
page of https://fantasy.mlssoccer.com/#stats-center'''

import pandas as pd
import numpy as np

import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome

from typing import List, Tuple

import matplotlib.pyplot as plt

def clean_data(text: str) -> List[str]:
    '''Will receive a string and convert to a list of strings with the 
    totals for each category for the specific game.
    '''
    word = ''
    dont_want = ['\t', '\n', '\\']
    row = []
    for char in text:
        if char not in dont_want:
            word += char
            if word == '-':
                row.append(word)
                word = ''
        elif word:
            row.append(word)
            word = ''
    return row

def update_negative_scores(game: List) -> List:
    '''Check row of game summary data for a hyphen to indicate a negative score, 
    and then update the row for the negative score for the game, and correct 
    the length of the row to match the rest of the table.
    '''
    #game = clean_data(game)

    if game[3] == '-':
        game[4] = '-' + game[4]
        game[3:] = game[4:]
    return game

def get_weekly_info(page_table_obj, week: int) -> List[str]:
    pass
    # return clean_data(page_table_obj[week]) + 
    # [int(entry) for entry in clean_data(page_table_obj[week + 37])[0::2]]

def get_player_salary(player_info: str) -> float:
    '''Method will receive the raw string from the player's info and return 
    the salary as a float
    '''

    assert type(player_info[2]) == str, "input needs to be a string"
    assert len(player_info[2]) > 3, "input is not the salary text "
    
    sal = ''
    for char in player_info[2][-2::-1]:
        if char != " ":
            sal = char + sal
        else:
            return float(sal)
    return float(sal)

def get_player_team(player_info: str) -> str:
    '''Method will receive the raw string from the player's info and return 
    the team as a str
    '''
    
    assert type(player_info[0]) == str, "input needs to be a string"
    assert len(player_info[0]) > 0, "input cannot be empty"
    
    return player_info[0]

def get_player_position(player_info: str) -> str:
    '''Method will receive the raw string from the player's info and return 
    their position as an initial.
    
    G is for Goalkeeper
    D is for Defender
    M is for Midfielder
    F is for Forward
    '''
    
    assert type(player_info[1]) == str, "input needs to be a string"
    assert len(player_info[1]) > 0, "input cannot be empty"
    
    return player_info[1][0]

def get_player_info(raw_player_data: List[str]) -> Tuple[str, float]:
    '''Will receive a string and break out the team position, player salary, 
    weekly salary change, and season salary change
    '''
    pass

