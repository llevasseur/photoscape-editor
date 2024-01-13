
import os
import json
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from helpers import *

cwd = os.getcwd()

DEBUG = 1

def getDataFromSite(data, site):
    home = van_record = other_team = other_record = ''
    time = month = day = year = date = ''

    driver = webdriver.Chrome()
    driver.get(site)
    assert "Canucks" and "ESPN" in driver.title

    # Set window size to small so Teams are listed as Acronyms
    driver.set_window_size(800, 800)

    # Fetch Gamestrip
    gamestrip = driver.find_element(By.XPATH, ".//div[contains(@class, 'Gamestrip')]")
    
    # Fetch h2_list which are the two teams
    h2_list = gamestrip.find_elements(By.XPATH, ".//h2[contains(@class, 'ScoreCell__TeamName')]")

    # Fetch records
    records = gamestrip.find_elements(By.XPATH, ".//div[contains(@class, 'Gamestrip__Record')]")
    
    # AWAY TEAM is h2_list[0]
    if (h2_list[0].text == 'VAN'):
        home, other_team = 'AWAY', h2_list[1].text
        van_record = records[0].text.split(',')[0]
        other_record = records[1].text.split(',')[0]

    # HOME TEAM is h2_list[1]
    else:
        home, other_team = 'HOME', h2_list[0].text
        van_record = records[1].text.split(',')[0]
        other_record = records[0].text.split(',')[0]

        return False

    # DATE
    game_info = driver.find_element(By.XPATH, ".//div[contains(@class, 'GameInfo__Meta')]")
    
    # Date is the first span in game_info
    date_text = game_info.find_elements(By.TAG_NAME, "span")[0].text
    
    # Parse the date string
    parsed_date = datetime.strptime(date_text, '%I:%M %p, %B %d, %Y')

    # Extract individual components
    month = parsed_date.strftime('%B')
    day = parsed_date.day
    year = parsed_date.year
    time = parsed_date.strftime('%I:%M %p').lstrip('0') # Time with AM/PM with no leading zeros
    date = f'{parsed_date.strftime("%b").lower()}{day}-{str(year)[-2:]}'

    # Remember to close the driver
    driver.quit()

    # Set data
    data["CANUCKS"] = {
        "TEAM": "VAN",
        "HOME" : home,
        "RECORD": van_record
    }

    data["OTHER"] = {
        "TEAM": other_team,
        "RECORD": other_record
    }

    data["DATE"] = {
        "TIME": time,
        "MONTH": month,
        "DAY": day,
        "YEAR": year
    }
    if valid_date(date):
        return date

    return False

def main():
    # Get user input for a URL
    site = input("Enter an ESPN URL: ")

    data = {}

    # Update data structure and get date to be used as dir name
    date_file = getDataFromSite(data, site)

    if not date_file:
        return
    
    # Create directory for game date
    destination = cwd + f'/json/games/{date_file}/'
    create_directory(destination)

    # Dump data to game-day.json
    with open(cwd + f'/json/games/{date_file}/game-day.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

        print(f'''
        Preview data has been fetched from ESPN and saved to games/{date_file}/game-day.json
        ''')
    
    return


if __name__ == '__main__':
    main()