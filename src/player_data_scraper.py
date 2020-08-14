"""Code for the scraper portion of getting stats from the fantasy soccer
page of https://fantasy.mlssoccer.com/#stats-center"""

import pandas as pd
import numpy as np

import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome

from typing import List, Tuple

import matplotlib.pyplot as plt


def clean_data(text: str) -> List[str]:
    """Will receive a string and convert to a list of strings with the 
    totals for each category for the specific game.
    """
    word = ""
    dont_want = ["\t", "\n", "\\"]
    row = []
    for char in text:
        if char not in dont_want:
            word += char
            if word == "-":
                row.append(word)
                word = ""
        elif word:
            row.append(word)
            word = ""
    return row


def update_negative_scores(game: List) -> List:
    """Check row of game summary data for a hyphen to indicate a negative score, 
    and then update the row for the negative score for the game, and correct 
    the length of the row to match the rest of the table.
    """
    # game = clean_data(game)

    if game[3] == "-":
        game[4] = "-" + game[4]
        game[3:] = game[4:]
    return game


def get_weekly_info(page_table_obj, week: int) -> List[str]:
    pass
    # return clean_data(page_table_obj[week]) +
    # [int(entry) for entry in clean_data(page_table_obj[week + 37])[0::2]]


def get_player_salary(player_info: str) -> float:
    """Method will receive the raw string from the player's info and return 
    the salary as a float
    """

    assert type(player_info[2]) == str, "input needs to be a string"
    assert len(player_info[2]) > 3, "input is not the salary text "

    sal = ""
    for char in player_info[2][-2::-1]:
        if char != " ":
            sal = char + sal
        else:
            return float(sal)
    return float(sal)


def get_player_team(player_info: str) -> str:
    """Method will receive the raw string from the player's info and return 
    the team as a str
    """

    assert type(player_info[0]) == str, "input needs to be a string"
    assert len(player_info[0]) > 0, "input cannot be empty"

    return player_info[0]


def get_player_position(player_info: str) -> str:
    """Method will receive the raw string from the player's info and return 
    their position as an initial.
    
    G is for Goalkeeper
    D is for Defender
    M is for Midfielder
    F is for Forward
    """

    assert type(player_info[1]) == str, "input needs to be a string"
    assert len(player_info[1]) > 0, "input cannot be empty"

    return player_info[1][0]


def get_player_info(raw_player_data: List[str]) -> Tuple[str, float]:
    """Will receive a string and break out the team position, player salary, 
    weekly salary change, and season salary change
    """
    pass


#### - the following functions go to the website and scrape data for players


# todo - refactor function to take appropriate div class, based on scraping for weekly data, updated metadata,
# or updated top stats data


def get_all_player_stats(
    web_driver: Chrome,
    player_ids: List[List[str]],
    week_first: int,
    week_last: int,
) -> List[List[str]]:
    """Function to go to the web and pull all players and stats for the players, by week, from the MLS
    Fantasy League website. 
    Must use a driver that is logged in to the site.
    Must use the full mls_player_ids which includes ID, player's name, and team for each player.
    
    For player data, use string 'div.row-table'.
    For player metadata, use string 'div.player-info-wrapper'.
    For player top stats, use string 'div.profile-top-stats'.
    """
    player_stats = []

    page_link = "https://fantasy.mlssoccer.com/#stats-center/player-profile/"

    # taking the list of mls_players, and adding the ID to the end of the page_link string in order to navigate to
    # that page. Can use this to cycle through all the player pages to amass weekly stats
    for player in player_ids:
        # print(page_link)
        # print(player[0])
        web_driver.get(page_link + player[0])
        time.sleep(5)

        # on the specific player page, create a page object for beautifulsoup to parse for the content
        html = web_driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # using the beautiful soup object to get the specific player details. will use this over and over to scrape and
        # store all the players data
        table = soup.select("div.row-table")
        table_text = [stats.text for stats in table]

        # in table_text, index 1 is the first game of the season in terms of info on the game, and index 38
        # (so index i + 37) is the associated per category stats for the match
        # each row will have the player's id, player name, team, information regarding the specific match, and then
        # respective category totals for that match
        for week in range(week_first, week_last + 1):
            if len(player_stats) % 50 == 0:
                print(
                    f"Scraped {round(50 * len(player_stats) / len(player_ids), 2)}% so far"
                )
            player_stats.append(
                [player[0]]
                + [player[1]]
                + [player[2]]
                + pds.update_negative_scores(pds.clean_data(table_text[week]))
                + [stat for stat in pds.clean_data(table_text[week + 37])[0::2]]
            )

    return player_stats


# Now get all the player specific data, id, player name, team, position and current salary


def get_all_player_meta_data(
    web_driver: Chrome, player_ids: List[List[str]]
) -> List[List[str]]:
    """Function to go to the web and pull all players and stats for the players, by week, from the MLS
    Fantasy League website. 
    Must use a driver that is logged in to the site.
    Must use the full mls_player_ids which includes ID, player's name, and team for each player.
    
    For player data, use string 'div.row-table'.
    For player metadata, use string 'div.player-info-wrapper'.
    For player top stats, use string 'div.profile-top-stats'."""

    player_data = []

    page_link = "https://fantasy.mlssoccer.com/#stats-center/player-profile/"

    # taking the list of mls_players, and adding the ID to the end of the page_link string in order to navigate to
    # that page. Can use this to cycle through all the player pages to amass weekly stats
    for player in player_ids:
        # print(page_link)
        # print(player[0])
        web_driver.get(page_link + player[0])
        time.sleep(5)

        # on the specific player page, create a page object for beautifulsoup to parse for the content
        html = web_driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # using the beautiful soup object to get the specific player details. will use this over and over to scrape and
        # store all the players data
        player_metadata = soup.select("div.player-info-wrapper")
        metadata_text = [meta.text for meta in player_metadata]
        # now we go through and clean up the meta data, and include it in the new table with each player
        if len(player_data) % 25 == 0:
            print(
                f"Scraped {100 * round(len(player_data) / len(player_ids), 2)}% so far"
            )
        player_data.append(
            [player[0]]
            + [player[1]]
            + [player[2]]
            + [pds.get_player_position(pds.clean_data(metadata_text[0]))]
            + [pds.get_player_salary(pds.clean_data(metadata_text[0]))]
        )
    return player_data


# todo - refactor function to take appropriate div class, based on scraping for weekly data, updated metadata,
# or updated top stats data


def get_all_player_top_stats(
    web_driver: Chrome, player_ids: List[List[str]]
) -> List[List[str]]:
    """Function to go to the web and pull all players and stats for the players, by week, from the MLS
    Fantasy League website. 
    Must use a driver that is logged in to the site.
    Must use the full mls_player_ids which includes ID, player's name, and team for each player.
    
    For player data, use string 'div.row-table'.
    For player metadata, use string 'div.player-info-wrapper'.
    For player top stats, use string 'div.profile-top-stats'.
    """
    player_stats = []

    page_link = "https://fantasy.mlssoccer.com/#stats-center/player-profile/"

    # taking the list of mls_players, and adding the ID to the end of the page_link string in order to navigate to
    # that page. Can use this to cycle through all the player pages to amass weekly stats
    for player in player_ids:
        # print(page_link)
        # print(player[0])
        web_driver.get(page_link + player[0])
        time.sleep(5)

        # on the specific player page, create a page object for beautifulsoup to parse for the content
        html = web_driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # using the beautiful soup object to get the specific player details. will use this over and over to scrape and
        # store all the players data
        table = soup.select("div.profile-top-stats")
        table_text = [stats.text for stats in table]

        if len(player_stats) % 25 == 0:
            print(
                f"Scraped {round(100 * len(player_stats) / len(player_ids), 2)}% so far"
            )
        player_stats.append(
            [player[0]]
            + [player[1]]
            + [player[2]]
            + pds.clean_data(table_text[0])
        )

    return player_stats
