import numpy as np
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains

from typing import List, Tuple, Dict

# urls, passwords, team names
mls_fantasy_url = "https://fantasy.mlssoccer.com/#"
# login_id = need to proper include for session
# pwd = need to proper include for session

TEAMS = {1: 'Atlanta United FC', 
 2: 'Chicago Fire FC', 
 3: 'FC Cincinnati', 
 4: 'Columbus Crew SC', 
 5: 'D.C. United', 
 6: 'Inter Miami CF', 
 7: 'Montreal Impact', 
 8: 'New England Revolution', 
 9: 'New York City FC', 
 10: 'New York Red Bulls', 
 11: 'Orlando City SC', 
 12: 'Philadelphia Union', 
 13: 'Toronto FC', 
 14: 'Colorado Rapids', 
 15: 'FC Dallas', 
 16: 'Houston Dynamo', 
 17: 'LA Galaxy', 
 18: 'Los Angeles FC', 
 19: 'Minnesota United FC', 
 20: 'Nashville SC', 
 21: 'Portland Timbers', 
 22: 'Real Salt Lake', 
 23: 'San Jose Earthquakes', 
 24: 'Seattle Sounders FC', 
 25: 'Sporting Kansas City', 
 26: 'Vancouver Whitecaps FC'}


def mls_fantasy_login(login_id: str,
        password: str, 
        mls_fantasy_url: str = "https://fantasy.mlssoccer.com/#") -> Chrome:
    '''
    Will log into the MLS fantasy page with login_id and password inputted from the user.
    Returns a Chrome webdriver which can be used to logout.
    '''
    
    # open a chrome browser and go to the mls fantasy landing page
    driver = Chrome()
    driver.get(mls_fantasy_url)
    driver.find_element_by_link_text('LOG IN').click()
    # send in login id and password and go into the browser
    time.sleep(3)
    username = driver.find_element_by_name('username')
    username.clear()
    username.send_keys(login_id)
    time.sleep(3)
    passcode = driver.find_element_by_name('password')
    passcode.clear()
    passcode.send_keys(password)
    driver.find_element_by_class_name('gigya-input-submit').click()
    
    return driver

def logout(web_driver: Chrome) -> None:
    '''
    Will logout out of the fantasy page when done with work.
    web_driver in this case is the browser that is launched with the mls fantasy page
    '''
    
    action = ActionChains(web_driver)
    
    first_menu = web_driver.find_element_by_class_name('my-account')
    action.move_to_element(first_menu).perform()
    time.sleep(2)
    
    second_menu = web_driver.find_element_by_css_selector('.fa.fa-power-off')
    action.move_to_element(second_menu)
    time.sleep(2)
    
    second_menu.click()

def scrape_team_stats(web_driver: Chrome) -> Dict[str, List[str]]:
    '''
    Create a dictionary with the player's MLS Fantasy soccer id as a key in
    a dictionary, and then a list of strings of the player's name and team as 
    the value.
    '''
    player_ids = {}

    web_driver.find_element_by_link_text('STATS CENTER').click()
    time.sleep(2)

    select_team = Select(web_driver.find_element_by_id('js-filter-squads'))
    select_team.select_by_visible_text(TEAMS[1])
    
    for team in range(1, 27):
        select_team.select_by_visible_text(TEAMS[team])

        html = web_driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        for tag in soup.select('a.player-name.js-player-modal'):
            player_ids[tag['data-player_id']] = \
                [' '.join(tag.text.strip('\n').split()[:-6]), TEAMS[team]]

    return player_ids
