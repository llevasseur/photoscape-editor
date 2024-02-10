# Fetch player data for canucks

import json
import os
import traceback

from helpers import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

cwd = os.getcwd()

ot = False
so = False
home = 'HOME'
van_score = 0
other_score = 0
date_file = ''
date_obj = {}

DEBUG = 1
error = 'Undefined'

def find_nav_index( li_list, txt ):
    # Robust change to determine index based on text.
    for i in range( 0, len( li_list ) ):
        index = i
        try:
            found = li_list[ i ].find_element( By.XPATH, f'.//span[contains(text(), {txt})]' )
            return index

        except:
            continue
    return False

def get_final_score_data( data, site ):
    global ot, so, home, van_score, other_score, date_file, date_obj, error
    # Set Chrome driver and visit site
    driver = webdriver.Chrome()
    driver.get( site )

    # Confirm Canucks are playing and that it's an ESPN site
    assert 'Canucks' and 'ESPN' in driver.title

    # Set window size to mid-big so Team Stats are listed
    driver.set_window_size( 1200, 1200 )

    # Confirm site is loaded
    timeout = 3
    try:
        element_present = EC.presence_of_element_located(( By.XPATH, './/div[ contains( @class, "Gamestrip" ) ]' ))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
        error = "Timed out waiting for ESPN Gamecast to load. Make sure the link is correct or increase allotted time."
        return False
    
    # Get Nav Bar
    nav = driver.find_element( By.XPATH, './/nav[ contains( @class, "Nav__Secondary" ) ]' )

    # Get li_list
    li_list = nav.find_elements( By.TAG_NAME, 'li' )


    index = find_nav_index( li_list, 'Team Stats' )
    if not index:
        error = 'Could not find Team Stats nav item.'
        return False

        # Noticed that it's not always in the 4th position
    driver.get( li_list[ index ].find_element( By.TAG_NAME, 'a' ).get_attribute( 'href' ) )

    # Confirm Canucks are playing and that it's an ESPN site
    assert 'Canucks' and 'Game Stats' and 'ESPN' in driver.title


    # Set window size to small so Teams are listed as Acronyms
    driver.set_window_size( 800, 800 )

    # Confirm site is loaded
    try:
        element_present = EC.presence_of_element_located(( By.XPATH, './/div[ contains( @class, "Gamestrip__Team--away" ) ]' ))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
        error = "Timed out waiting for ESPN Team Stats to load. Make sure the link is correct or increase allotted time."
        return False

    # Fetch Team Stats
# - The two teams
    away = driver.find_element( By.XPATH, './/div[ contains( @class, "Gamestrip__Team--away" ) ]' )
    away_content = away.find_element( By.XPATH, './/div[ contains(@class, "Gamestrip__TeamContent" ) ]')
    away_team = away_content.find_element( By.TAG_NAME, 'h2' ).text

    home_obj = driver.find_element( By.XPATH, './/div[ contains( @class, "Gamestrip__Team--home" ) ]' )
    home_content = home_obj.find_element( By.XPATH, './/div[ contains( @class, "Gamestrip__TeamContent" ) ]' )
    home_team = home_content.find_element( By.TAG_NAME, 'h2' ).text

    data[ 'CANUCKS' ] = {
        'SCORE': str( van_score ),
        'HOME': home,
        'WIN': 'True' if van_score > other_score else 'False',
        'OT': 'True' if ot else 'False',
        'SO': 'True' if so else 'False'
    }

    data[ 'OTHER' ] = {
        'TEAM': away_team if home == 'HOME' else home_team,
        'SCORE': str( other_score )
    }

    data[ 'DATE' ] = {
        'MONTH': date_obj[ 'MONTH' ][ :3 ],
        'DAY': date_obj[ 'DAY' ],
        'YEAR': date_obj[ 'YEAR' ]
    }

    stats_table = driver.find_element( By.XPATH, './/section[ contains( @class, "TeamStatsTable" ) ]' )
    stats = stats_table.find_element( By.XPATH, './/div[ contains( @class, "Table__Scroller" ) ]' )
    tbody = stats.find_element( By.XPATH, './/tbody[ contains( @class, "Table__TBODY" ) ]' )

    c_ind = 2 if home == 'HOME' else 1
    o_ind = 1 if home == 'HOME' else 2

    tr_list = tbody.find_elements( By.TAG_NAME, 'tr' )
    # SOG
    td_list = tr_list[ 0 ].find_elements( By.TAG_NAME, 'td' )

    data[ 'CANUCKS' ][ 'SOG' ] = td_list[ c_ind ].text
    data[ 'OTHER' ][ 'SOG' ] = td_list[ o_ind ].text

    # HITS
    td_list = tr_list[ 1 ].find_elements( By.TAG_NAME, 'td' )

    data[ 'CANUCKS' ][ 'HITS' ] = td_list[ c_ind ].text
    data[ 'OTHER' ][ 'HITS' ] = td_list[ o_ind ].text

    # PP OPPORTUNITIES
    td_list = tr_list[ 4 ].find_elements( By.TAG_NAME, 'td' )

    c_ppo = td_list[ c_ind ].text
    o_ppo = td_list[ o_ind ].text

    # PP GOALS
    td_list = tr_list[ 5 ].find_elements( By.TAG_NAME, 'td' )

    c_ppg = td_list[ c_ind ].text
    o_ppg = td_list[ o_ind ].text

    data[ 'CANUCKS' ][ 'PP' ] = f'{ c_ppg }/{ c_ppo }'
    data[ 'OTHER' ][ 'PP' ] = f'{ o_ppg }/{ o_ppo }'

    # PIM
    td_list = tr_list[ 9 ].find_elements( By.TAG_NAME, 'td' )

    data[ 'CANUCKS' ][ 'PIM' ] = td_list[ c_ind ].text
    data[ 'OTHER' ][ 'PIM' ] = td_list[ o_ind ].text

    # FACEOFFS
    td_list = tr_list[ 2 ].find_elements( By.TAG_NAME, 'td' )

    data[ 'CANUCKS' ][ 'FO' ] = td_list[ c_ind ].text
    data[ 'OTHER' ][ 'FO' ] = td_list[ o_ind ].text

    print( f'''
            FINAL SCORE Test: Passed
    ''' )

    # Remember to close the driver
    driver.quit()

    return True


def get_box_score_data( data, site ):
    global ot, so, home, van_score, other_score, date_file, error
    # Set Chrome driver and visit site
    driver = webdriver.Chrome()
    driver.get( site )

    # Confirm Canucks are playing and that it's an ESPN site
    assert 'Canucks' and 'ESPN' in driver.title

    # Set window size to small so Teams are listed as Acronyms
    driver.set_window_size( 800, 800 )

    # Initialize test_case
    test_case = 'DATE'

    # Confirm site is loaded
    timeout = 3
    try:
        element_present = EC.presence_of_element_located(( By.XPATH, './/nav[ contains( @class, "Nav__Secondary" ) ]' ))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
        error = "Timed out waiting for ESPN Gamecast to load. Make sure the link is correct or increase allotted time."
        return False

    # Get Nav Bar
    nav = driver.find_element( By.XPATH, './/nav[ contains( @class, "Nav__Secondary" ) ]' )
    
    # Get li_list
    li_list = nav.find_elements( By.TAG_NAME, 'li' )

    # Determine if it's live by checking if navbar has Recap option
    index = find_nav_index( li_list,  'Recap')
    live = False
    if not index:
        live = True

    try:
        # DATE
        game_info = driver.find_element( By.XPATH, './/div[ contains( @class, "GameInfo__Meta" ) ]' )

        # Date is the first span in game_info
        date_text = game_info.find_elements( By.TAG_NAME, 'span' )[ 0 ].text

        # Parse the date string
        try:
            # Try the first format: '1:00 PM, 13 January 2024'
            parsed_date = datetime.strptime( date_text, '%I:%M %p, %d %B %Y' )
        except ValueError:
            # If the first format fails, try the second format: '4:00 PM, January 11, 2024'
            parsed_date  = datetime.strptime( date_text, '%I:%M %p, %B %d, %Y' )

        # Set data

        # Extract date using helper.get_date_json
        # Returns date_file
        date_file = get_date_json( data, parsed_date )

        if not valid_date( date_file ):
            error = f'Invalid date: {date_file}'
            return False

        print( f'''
            { test_case } Test         : Passed
        ''' )

        test_case = 'HOME or AWAY'

        with open( cwd + f'/json/games/{ date_file }/game-day.json', 'r' ) as json_file:
            # Determine if canucks are HOME or AWAY
            file = json.load( json_file )
            home = file.get( 'CANUCKS' )[ 'HOME' ]

        print( f'''
            { test_case } Test : Passed
            HOME: { home }
        ''' )

        # Fetch Goal Info ( BOX SCORE )
        #    - Keep track of the score for AWAY and HOME, away is first home is second
        #    - for each tr, increment PERIOD, unless PERIOD = 5, then break. and get td_list
        #    - if td_list[ 0 ] does not has div w class playByPlay__text-assists.getText, continue
        #    - td_list[ 0 ].getText = time of goal
        #    - td_list[ 2 ].getText = First name initial. Last name Type of Goal ( if there )
        #    - for td_list[ 2 ], get span_list[ 0 ].getText as number of goals that player has scored and
        #    - if that text is not 'Unassisted'
        #    - Take the substring after \n and split by ','
        #    - These are the assistors and their number of assists
        #    - if td_list[ 3 ].getText != away goal total, list as an away goal and increment away goal, else, list as a home goal and increment home goal

        #   NOTE: If period = 4 period = OT and OT = True, if vanWin = True, winFinal = WIN ( OT ) else winFinal = LOSS ( OT )

        #   NOTE: If period = 5, period = SHOOTOUT and SHOOTOUT = True, if vanWin = True, winFinal = WIN ( SO ) else winFinal = LOSS ( SO )

        test_case = 'PERIODS'
        # Get div w class tabs__content
        goal_section = driver.find_element( By.XPATH, './/div[ contains( @class, "tabs__content" ) ]' )

        # Get each tbody w class Table__TBODY
        tbody_list = goal_section.find_elements( By.XPATH, './/tbody[ contains( @class, "Table__TBODY" ) ]' )

        # Initialize period lookup table
        periods = [ '1', '2', '3', 'OT', 'SHOOTOUT' ]
        # Start in 1st period = index 0
        p = 0
        # Reset van and other score to 0
        van_score = other_score = 0
        data[ 'CANUCKS' ] = []
        data[ 'OTHER' ] = []
        # Keep track of shootout markers
        van_so = other_so = 0

        print( f'''
            { test_case } Test      : Passed
        ''' )

        # Iterate through each period
        # Skip table[ 0 ] - Complete summary

        tbody_list = tbody_list[ 1: ]
        if live:
            # Check if tbody_list.thead.th w class=title == '1st PERIOD'
            period_list = goal_section.find_elements( By.XPATH, './/thead[ contains( @class, "Table__THEAD" ) ]' )
            period_title = period_list[ 1 ].find_element( By.XPATH, './/th[ contains( @class, "Table__TH" ) ]' ).text.lower()
            if ( period_title != '1st period' ):
                tbody_list.reverse()

        for i in range( 0, len( tbody_list ) ):
            # Define the period using index p and lookup dict
            period = periods[ p ]
            test_case = f'{ "PERIOD " if period != "SHOOTOUT" and period != "OT" else "" }{ period } GOALS'
            # Find each goal info ( or shootout attempt ) in period
            # tr_list = list of goals in this period
            tr_list = tbody_list[ i ].find_elements( By.XPATH, './/tr[ contains( @class, "playByPlay__tableRow" ) ]' )

            print( f'''
            GET { test_case }    : Passed
            ''' )

            # Determine if OT and SO are true
            if p > 2:
                ot = True
                if p == 4:
                    so = True
                    # Create data objects
                    data[ 'CANUCKS' ].append( {
                        'PERIOD': 'SHOOTOUT',
                        'SCORERS': []
                    } )
                    canucks_so_index = len( data[ 'CANUCKS' ] ) - 1

                    data[ 'OTHER' ].append( {
                        'PERIOD': 'SHOOTOUT',
                        'SCORERS': []
                    } )
                    other_so_index = len( data[ 'OTHER' ] ) - 1

            # Check if the game is live, if so, goals are listed in reverse order
            if live:
                if ( period_title != '1st period' ):
                    tr_list.reverse()

            # Iterate through each goal of the period
            for j in range( 0, len( tr_list ) ):
                test_case = f'GOAL { j+1 }'
                # Find the list of stats in the goal info
                td_list = tr_list[ j ].find_elements( By.TAG_NAME, 'td' )

                # Handle shootout first
                if so:
                    test_case = 'SO SCORER'

                    shooter = extract_second_word( td_list[ 1 ].text ).upper()

                    # Check if the shootout counter changes
                    # Update data if so
                    if home == 'AWAY':
                        if td_list[ 2 ].text != str( van_so ):
                            data[ 'CANUCKS' ][ canucks_so_index ].get( 'SCORERS' ).append( shooter )
                            van_so += 1

                        elif td_list[ 3 ].text != str( other_so ):
                            data[ 'OTHER' ][ other_so_index ].get( 'SCORERS' ).append( shooter )
                            other_so += 1

                    else:
                        if td_list[ 3 ].text != str( van_so ):
                            data[ 'CANUCKS' ][ canucks_so_index ].get( 'SCORERS' ).append( shooter )
                            van_so += 1

                        elif td_list[ 2 ].text != str( other_so ):
                            data[ 'OTHER' ][ other_so_index ].get( 'SCORERS' ).append( shooter )
                            other_so += 1

                    print( f'''
            { test_case } Test    : Passed
                            ''' )

                # Determine if goals were scored
                else:
                    test = td_list[ 0 ].text

                    if not test == 'No Goals Scored':
                        # Identified a goal scorer this period
                        test_case = 'SET DATA'
                        obj = {}

                        if home == 'AWAY':
                            if td_list[ 3 ].text != str( van_score ):
                                obj[ 'PERIOD' ] = period
                                obj[ 'TIME' ] = td_list[ 0 ].text
                                get_scorer_and_assistors( obj, td_list[ 2 ].text, False )

                                data.get( 'CANUCKS' ).append( obj )
                                van_score += 1

                            else:
                                obj[ 'PERIOD' ] = period
                                obj[ 'TIME' ] = td_list[ 0 ].text
                                get_scorer_and_assistors( obj, td_list[ 2 ].text, True )

                                data.get( 'OTHER' ).append( obj )
                                other_score += 1

                        # Else Vancouver is HOME
                        else:
                            if td_list[ 4 ].text != str( van_score ):
                                obj[ 'PERIOD' ] = period
                                obj[ 'TIME' ] = td_list[ 0 ].text
                                get_scorer_and_assistors( obj, td_list[ 2 ].text, False )

                                data.get( 'CANUCKS' ).append( obj )
                                van_score += 1

                            # Other scored
                            else:
                                obj[ 'PERIOD' ] = period
                                obj[ 'TIME' ] = td_list[ 0 ].text
                                get_scorer_and_assistors( obj, td_list[ 2 ].text, True )

                                data.get( 'OTHER' ).append( obj )
                                other_score += 1

                        print( f'''
            { test_case } Test    : Passed
                            ''' )
            if ( so ):
                van_score += 1 if van_so > other_so else 0
                other_score += 1 if van_so < other_so else 0
            # Increment period index
            p += 1


    except Exception as e:

        print( f'''
        { test_case } Test : Failed
        ''' )
        traceback.print_exc()
        error = e
        return False



    # Remember to close the driver
    driver.quit()

    return True

def fetch_box_score( site ):
    global date_file, date_obj
    data = {}

    # Update data structure and get date to be used as dir name
    test = get_box_score_data( data, site )

    if not test:
        return False

    # Create directory for game date
    destination = cwd + f'/json/games/{ date_file }/'
    create_directory( destination )

    # Dump data to game-day.json
    with open( cwd + f'/json/games/{ date_file }/box-score.json', 'w' ) as json_file:
        json.dump( data, json_file, indent=4 )

        print( f'''
        Preview data has been fetched from ESPN and saved to games/{ date_file}/box-score.json
        ''' )

    date_obj = data[ 'DATE' ]

    return True

def fetch_final_score( site ):
    global date_file
    data = {}

    # Update data structure and get date to be used as dir name
    test = get_final_score_data( data, site )

    if not test:
        return False

    # Create directory for game date
    destination = cwd + f'/json/games/{ date_file }/'
    create_directory( destination )

    # Dump data to game-day.json
    with open( cwd + f'/json/games/{ date_file }/final-score.json', 'w' ) as json_file:
        json.dump( data, json_file, indent=4 )

        print( f'''
        Preview data has been fetched from ESPN and saved to games/{ date_file }/final-score.json
        ''' )

    return True

def main():
    global error
    print( f'''
############################################################

                FETCH FINAL SCORE AND BOX SCORE DATA

############################################################
    ''' )
    # Get user input for a URL
    site = input( '\nENTER URL: ' )

    if not fetch_box_score( site ):
        print(f"Oh no! Could not fetch box score. Error: {error} ")
        return

    if not fetch_final_score( site ):
        print(f"Oh no! Could not fetch final score. Error: {error} ")
        return

    return

if __name__ == '__main__':
    main()
