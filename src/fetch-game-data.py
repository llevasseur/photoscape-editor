# Fetch player data for canucks
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import json
import os
import traceback

from helpers import *

cwd = os.getcwd()

ot = False 
so = False
home = 'HOME'
van_score = 0
other_score = 0

DEBUG = 1

def get_final_score_date(data, site):
    return
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

def get_box_score_data(data, site):
    global ot, so, home, van_score, other_score
    # Set Chrome driver and visit site
    driver = webdriver.Chrome()
    driver.get(site)
    
    # Confirm Canucks are playing and that it's an ESPN site
    assert "Canucks" and "ESPN" in driver.title

    # Set window size to small so Teams are listed as Acronyms
    driver.set_window_size(800, 800)

    # Initialize test_case
    test_case = 'DATE'

    try:
        # DATE
        game_info = driver.find_element(By.XPATH, ".//div[contains(@class, 'GameInfo__Meta')]")
        
        # Date is the first span in game_info
        date_text = game_info.find_elements(By.TAG_NAME, "span")[0].text
        
        # Parse the date string
        parsed_date = datetime.strptime(date_text, '%I:%M %p, %B %d, %Y')

        # Set data

        # Extract date using helper.get_date_json
        # Returns date_file
        date_file = get_date_json(data, parsed_date)

        if not valid_date(date_file):
            return False
        
        print(f'''
            {test_case} Test         : Passed
        ''')

        test_case = 'HOME or AWAY'
        
        with open(cwd + f'/json/games/{date_file}/game-day.json', 'r') as json_file:
            # Determine if canucks are HOME or AWAY
            file = json.load(json_file)
            home = file.get('CANUCKS')['HOME']
        
        print(f'''
            {test_case} Test : Passed
        ''')
        
        # Fetch Goal Info (BOX SCORE)
        #    - Keep track of the score for AWAY and HOME, away is first home is second
        #    - for each tr, increment PERIOD, unless PERIOD = 5, then break. and get td_list
        #    - if td_list[0] does not has div w class playByPlay__text-assists.getText, continue
        #    - td_list[0].getText = time of goal
        #    - td_list[2].getText = First name initial. Last name Type of Goal (if there)
        #    - for td_list[2], get span_list[0].getText as number of goals that player has scored and 
        #    - if that text is not "Unassisted"
        #    - Take the substring after \n and split by ','
        #    - These are the assistors and their number of assists
        #    - if td_list[3].getText != away goal total, list as an away goal and increment away goal, else, list as a home goal and increment home goal
            
        #   NOTE: If period = 4 period = OT and OT = True, if vanWin = True, winFinal = WIN (OT) else winFinal = LOSS (OT)

        #   NOTE: If period = 5, period = SHOOTOUT and SHOOTOUT = True, if vanWin = True, winFinal = WIN (SO) else winFinal = LOSS (SO)

        test_case = 'PERIODS'
        # Get div w class tabs__content
        goal_section = driver.find_element(By.XPATH, ".//div[contains(@class, 'tabs__content')]")
        
        # Get each tbody w class Table__TBODY
        tbody_list = goal_section.find_elements(By.XPATH, ".//tbody[contains(@class, 'Table__TBODY')]")

        # Initialize period lookup table
        periods = ['1', '2', '3', 'OT', 'SHOOTOUT']
        # Start in 1st period = index 0
        p = 0
        # Reset van and other score to 0
        van_score = other_score = 0
        data['CANUCKS'] = []
        data['OTHER'] = []

        print(f'''
            {test_case} Test      : Passed
        ''')

        # Iterate through each period
        # Skip table[0] - Complete summary

        for i in range(1, len(tbody_list)):
            # Define the period using index p and lookup dict
            period = periods[p]
            test_case = f'{period} GOALS'
            # Find each goal info (or shootout attempt) in period
            # tr_list = list of goals in this period
            tr_list = tbody_list[i].find_elements(By.XPATH, ".//tr[contains(@class, 'playByPlay__tableRow')]")

            print(f'''
            {test_case} Test    : Passed
            ''')

            # Determine if OT and SO are true
            if p > 2:
                ot = True
                if p == 4:
                    so = True
                    
                    # Keep track of shootout markers
                    van_so = other_so = 0

            # Iterate through each goal of the period
            for j in range(0, len(tr_list)):
                test_case = f'GOAL {j+1}'
                # Find the list of stats in the goal info
                td_list = tr_list[j].find_elements(By.TAG_NAME, 'td')
                
                # Handle shootout first
                # TODO Test
                if so:
                    test_case = 'SHOOTOUT'

                    # Initialize shootout scorer objects
                    data.get('CANUCKS').append({
                        "PERIOD": "SHOOTOUT",
                        "SCORERS": []

                    })
                    data.get('OTHER').append({
                        "PERIOD": "SHOOTOUT",
                        "SCORERS": []
                    })
                    # Determine shootout object index using dict len
                    c_len = len(data.get('CANUCKS'))
                    o_len = len(data.get('OTHER'))

                    shooter = extract_second_word(td_list[1].text)
                    # Check if the shootout counter changes
                    # Update data if so
                    if home == 'False':
                        if td_list[2].text != str(van_so):
                            data.get('CANUCKS')[c_len - 1].get("SCORERS").append(shooter)
                            van_so += 1

                        elif td_list[3].text != str(other_so):
                            data.get('OTHER')[o_len - 1].get("SCORERS").append(shooter)
                            other_so += 1

                    elif home == 'True':
                        if td_list[3].text != str(van_so):
                            data.get('CANUCKS')[c_len - 1].get("SCORERS").append(shooter)
                            van_so += 1

                        elif td_list[2].text != str(other_so):
                            data.get('OTHER')[o_len - 1].get("SCORERS").append(shooter)
                            other_so += 1


                # Determine if goals were scored
                else:
                    test = td_list[0].text

                    if not test == 'No Goals Scored':
                        # Identified a goal scorer this period
                        test_case = 'SET DATA'
                        obj = {}

                        if home == 'False':
                            if td_list[3].text != str(van_score):
                                obj['PERIOD'] = period
                                obj['TIME'] = td_list[0].text
                                get_scorer_and_assistors(obj, td_list[2].text, False)

                                data.get('CANUCKS').append(obj)
                                van_score += 1
                            
                            else:
                                obj['PERIOD'] = period
                                obj['TIME'] = td_list[0].text
                                get_scorer_and_assistors(obj, td_list[2].text, True)

                                data.get('OTHER').append(obj)
                                other_score += 1
                        
                        # Else Vancouver is HOME
                        else:
                            if td_list[4].text != str(van_score):
                                obj['PERIOD'] = period
                                obj['TIME'] = td_list[0].text
                                get_scorer_and_assistors(obj, td_list[2].text, False)

                                data.get('CANUCKS').append(obj)
                                van_score += 1
                            
                            # Other scored
                            else:
                                obj['PERIOD'] = period
                                obj['TIME'] = td_list[0].text
                                get_scorer_and_assistors(obj, td_list[2].text, True)

                                data.get('OTHER').append(obj)
                                other_score += 1

                            print(f'''
            {test_case} Test    : Passed
            {obj}
                            ''')

            # Increment period index
            p += 1

    except Exception as e:

        print(f'''
        {test_case} Test : Failed
        {e}
        ''')
        traceback.print_exc()
        return False
    
    

    # Remember to close the driver
    driver.quit()

    return date_file

def fetch_box_score(site):
    data = {}

    # Update data structure and get date to be used as dir name
    date_file = get_box_score_data(data, site)

    if not date_file:
        return
    
    # Create directory for game date
    destination = cwd + f'/json/games/{date_file}/'
    create_directory(destination)

    # Dump data to game-day.json
    with open(cwd + f'/json/games/{date_file}/box-score.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

        print(f'''
        Preview data has been fetched from ESPN and saved to games/{date_file}/box-score.json
        ''')
    return

def fetch_final_score(site):
    data = {}

    # Update data structure and get date to be used as dir name
    date_file = False

    if not date_file:
        return
    
    # Create directory for game date
    destination = cwd + f'/json/games/{date_file}/'
    create_directory(destination)

    # Dump data to game-day.json
    with open(cwd + f'/json/games/{date_file}/final-score.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

        print(f'''
        Preview data has been fetched from ESPN and saved to games/{date_file}/final-score.json
        ''')

def main():
    players = {}

    # Get user input for a URL
    site = input("Enter an ESPN URL: ")

    fetch_box_score(site)

    fetch_final_score(site)
    
    return

if __name__ == "__main__":
    main()