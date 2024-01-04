# Fetch player data for canucks
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import requests
from bs4 import BeautifulSoup
import re
import json
import os

# Fetch Team Stats
# - The two teams
#    - AWAY
#    - div w class Gamestrip__Team--away
#    - div w class Gamestrip__TeamContent
#    - h2.get text = {away team acronym}
#    - {lowercase}.png use to fetch logo
#    - if VAN - vanHome = false

#    - HOME
#    - div w class Gamestrip__Team--home
#    - div w class Gamestrip__TeamContent
#    - h2.get text = {home team acronym}
#    - {lowercase}.png use to fetch logo

# - Final Score between the two teams
#    - AWAY
#    - div w class Gamestrip__Team--away
#    - div w class Gamestrip__ScoreContainer
#    - get text = {away score}

#    - HOME
#    - div w class Gamestrip__Team--home
#    - div w class Gamestrip__ScoreContainer
#    - get text = {home score}
#    - if {home score} > {away score} XOR vanHom: vanWin = true


#    - div w class PageLayout__Main
# STATS
#    - section w class TeamStatsTable, get tr_list

# - Shots for both teams
#    - tr_list[0] get td_list
#    - "Shots" = td_list[0].getText
#    - AWAY SHOTS = td_list[1].getText
#    - HOME SHOTS = td_list[2].getText

# - Hits for both teams
#    - tr_list[1] get td_list
#    - "Hits" = td_list[0].getText
#    - AWAY HITS = td_list[1]
#    - HOME HITS = td_list[2]

# - Faceoff wins for both teams
#    - tr_list[2] get td_list
#    - "Faceoffs Won" = td_list[0].getText
#    - AWAY FOW = td_list[1]
#    - HOME FOW = td_list[2]

# - Power-play opportunities
#    - tr_list[4] get td_list
#    - "Power Play Opportunities" = td_list[0].getText
#    - AWAY PPO = td_list[1]
#    - HOME PPO = td_list[2]

# - Power-play goals for both teams
#    - tr_list[5] get td_list
#    - "Power Play Goals" = td_list[0].getText
#    - AWAY PPG = td_list[1]
#    - AWAY PPRatio = "{AWAY PPG}/{AWAY PPO}
#    - HOME PPG = td_list[2]
#    - HOME PPRatio = "{HOME PPG}/{HOME PPO}"    

# GAME INFO
#    - main - section w class GameInfo
#    - div w class ContentList
#    - div w class GameInfo__Meta.getText
#    - filter out first two lines = "January 2, 2024"'
#    - filter out all but first 3 characters to get abbreviation
#    - Filter out text without first word and space to get day and year


# Fetch Goal Info

def main():
    players = {}
    
    return

if __name__ == "__main__":
    main()