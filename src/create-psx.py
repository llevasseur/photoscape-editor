## Version 0.0.1
## create-psx.py

import argparse
import os
import json
import traceback

from datetime import datetime
from helpers import *

cwd = os.getcwd()

DEBUG = 1

def update_logo( source, psxprj, i, logo_path, type ):
    # Copy logo into source
    copy_file_to_directory( logo_path, source )
    
    destination_file = os.path.basename( logo_path )

    # Reference logo basename in psxprj object
    psxprj.get( 'object' )[ '_v' ][ i ][ '_v' ][ 'image' ][ '_v' ][ '_v' ] = destination_file
    
    if ( DEBUG ):
        print( f'''
        Update { type } : Complete
        ''' )
    return

def update_text( psxprj, i, text, type ):
    # Reference new text in psxprj object
    psxprj.get( 'object' )[ '_v' ][ i ][ '_v' ][ 'text' ][ '_v' ] = text
    
    if ( DEBUG ):
        print( f'''
        Update { type } : Complete
        ''' )
    return

def make_shootout_text( stat, index = 0 ):
    # Bug: Need to x text boxes when line count = 3x
    # Note: First text box has SHOOTOUT\n
    text = ''
    if index == 0: 
        text += 'SHOOTOUT\n'
    scorers = stat.get( 'SCORERS' )
    for i in range( index, len( scorers ) ):
        text += scorers[ i ]
        if ( i != len( scorers ) - 1 ):
            text += '\n'

    return text

def make_scorer_text( stat, team ):
    text = ''
    periods = {
        '1': '1ST',
        '2': '2ND',
        '3': '3RD',
        'OT': 'OT',
        'SHOOTOUT': 'SHOOTOUT'
    }
    # Convert period into correct format
    period = periods.get( stat.get( 'PERIOD' ) )
    
    # Handle shootout
    if period == 'SHOOTOUT':
        return make_shootout_text( stat, team )
    
    # Handle other types of periods
    time = stat.get( 'TIME' )
    type = stat.get( 'TYPE' )
    scorer = stat.get( 'SCORER' )
    assistors = stat.get( 'ASSISTORS' )
    n = len( assistors )
    # CANUCKS Scorer
    if ( team == 'CANUCKS' ):
        # Construct text
        text += f'{ period } - '
        text += f'({ time })'
        text += f' { type }\n'
        text += f'G: { scorer }\n'
        text += 'A: '
        
        for i in range( 0, n ):
            text += f'{ assistors[ i ] }'
            if ( i != n - 1 ):
                text += ', '

    # OTHER Team Scorer
    else:
        # Construct text
        text += f'{ type } '
        text += f'({ time })'
        text += f' - { period }\n'
        text += f'{ scorer } :G\n'

        for i in range( 0, n ):
            text += f'{ assistors[ i ] }'
            if ( i != n - 1 ):
                text += ', ' 
        text += ' :A'   

    return text


def update_psxprj( selected_choice, source, date_file ):
    # Find psxprj from copied template source json
    with open( source + '/psxproject.json', 'r' ) as json_file:
        psxprj = json.load( json_file )
        
    # Get team logo data from team look-up json
    with open( cwd + '/json/look-up/teams.json', 'r' ) as logo_file:
        team_lookup = json.load( logo_file )

    # Get selected choice data from related json
    with open( cwd + f'/json/games/{ date_file }/{ selected_choice }.json', 'r' ) as stats_file:
        stats = json.load( stats_file )

    try:
        match selected_choice:
            case 'game-day':
                
                # Update VAN LOGO
                type = 'VAN Logo    '
                index = 0
                #NOTE Change IMG to ALT1, ALT2, ALT3
                logo = team_lookup.get( 'VAN' )[ 'IMG' ]
                update_logo( source, psxprj, index, logo, type )

                # Update OTHER LOGO
                other = stats.get( 'OTHER' )[ 'TEAM' ]
                type = f'{ other } Logo    '
                index = 1
                logo = team_lookup.get( stats.get( 'OTHER' )[ 'TEAM' ] )[ 'IMG' ]
                update_logo( source, psxprj, index, logo, type )
                
                # Delete OTHER.png from template
                os.remove( source + '/OTHER.png' )

                # Update TIME
                type = 'Time        '
                index = 9
                time = stats.get( 'DATE' )[ 'TIME' ]
                update_text( psxprj, index, time, type )

                # Update DATE
                type = 'Date        '
                index = 10
                date = f'{ stats.get( "DATE" )[ "MONTH" ] } { stats.get( "DATE" )[ "DAY" ] }, { stats.get( "DATE" )[ "YEAR" ] }'
                update_text( psxprj, index, date, type )

                # Update VAN RECORD
                type = 'VAN Record  '
                index = 13
                record = stats.get( 'CANUCKS' )[ 'RECORD' ]
                update_text( psxprj, index, record, type )

                # Update OTHER RECORD
                type = f'{ other } Record  '
                index = 14
                record = stats.get( 'OTHER' )[ 'RECORD' ]
                update_text( psxprj, index, record, type )

                # Update HOME or AWAY
                type = 'HOME or AWAY'
                index = 16
                where = stats.get( 'CANUCKS' )[ 'HOME' ]
                update_text( psxprj, index, where, type )
            
            case 'final-score':
                # Update VAN LOGO
                type = 'VAN Logo    '
                index = 0
                #NOTE Change IMG to ALT1, ALT2, ALT3
                logo = team_lookup.get( 'VAN' )[ 'IMG' ]
                update_logo( source, psxprj, index, logo, type )

                # Update OTHER LOGO
                # TODO Make a function
                other = stats.get( 'OTHER' )[ 'TEAM' ]
                type = f'{ other } Logo    '
                index = 1
                logo = team_lookup.get( stats.get( 'OTHER' )[ 'TEAM' ] )[ 'IMG' ]
                update_logo( source, psxprj, index, logo, type )

                # Delete OTHER.png from template
                os.remove( source + '/OTHER.png' )

                # Update VAN SCORE
                type = 'VAN Score   '
                index = 11
                score = stats.get( 'CANUCKS' )[ 'SCORE' ]
                update_text( psxprj, index, score, type )

                # Update OTHER SCORE
                type = f'{ other } Score   '
                index = 12
                score = stats.get( 'OTHER' )[ 'SCORE' ]
                update_text( psxprj, index, score, type )

                # Update VAN SOG
                type = 'VAN SOG     '
                index = 20
                sog = stats.get( 'CANUCKS' )[ 'SOG' ]
                update_text( psxprj, index, sog, type )

                # Update VAN HITS
                type = 'VAN HITS    '
                index = 21
                hits = stats.get( 'CANUCKS' )[ 'HITS' ]
                update_text( psxprj, index, hits, type )

                # Update VAN PP
                type = 'VAN PP      '
                index = 22
                pp = stats.get( 'CANUCKS' )[ 'PP' ]
                update_text( psxprj, index, pp, type )

                # Update VAN PIM
                type = 'VAN PIM     '
                index = 23
                pim = stats.get( 'CANUCKS' )[ 'PIM' ]
                update_text( psxprj, index, pim, type )

                # Update VAN FO
                type = 'VAN FO      '
                index = 24
                fo = stats.get( 'CANUCKS' )[ 'FO' ]
                update_text( psxprj, index, fo, type )

                # Update OTHER SOG
                type = f'{ other } SOG     '
                index = 25
                sog = stats.get( 'OTHER' )[ 'SOG' ]
                update_text( psxprj, index, sog, type )

                # Update OTHER HITS
                type = f'{ other } HITS    '
                index = 26
                hits = stats.get( 'OTHER' )[ 'HITS' ]
                update_text( psxprj, index, hits, type )

                # Update OTHER PP
                type = f'{ other } PP      '
                index = 27
                pp = stats.get( 'OTHER' )[ 'PP' ]
                update_text( psxprj, index, pp, type )

                # Update OTHER PIM
                type = f'{ other } PIM     '
                index = 28
                pim = stats.get( 'OTHER' )[ 'PIM' ]
                update_text( psxprj, index, pim, type )

                # Update OTHER FO
                type = f'{ other } FO      '
                index = 29
                fo = stats.get( 'OTHER' )[ 'FO' ]
                update_text( psxprj, index, fo, type )

                # Update DATE
                type = 'Date        '
                index = 30
                date = f'{ stats.get( "DATE" )[ "MONTH" ] } { stats.get( "DATE" )[ "DAY" ] }, { stats.get( "DATE" )[ "YEAR" ] }'
                update_text( psxprj, index, date, type )

                # Update HOME or AWAY
                type = 'HOME or AWAY'
                index = 31
                where = stats.get( 'CANUCKS' )[ 'HOME' ]
                update_text( psxprj, index, where, type )

                # Update WIN or LOSS
                type = 'WIN or LOSS '
                index = 33
                win = 'WIN' if stats.get( 'CANUCKS' )[ 'WIN' ] == 'True' else 'LOSS'
                if stats.get( 'CANUCKS' )[ 'OT' ] == 'True':
                    if stats.get( 'CANUCKS' )[ 'SO' ] == 'True':
                        win += ' ( SO )'
                    else:
                        win += ' ( OT )'
                update_text( psxprj, index, win, type )
            
            case 'box-score':
                # Create CANUCKS and OTHER SCORERS
                canucks_scorers = stats.get( 'CANUCKS' )
                other_scorers = stats.get( 'OTHER' )
                n = max( len( canucks_scorers ) // 7, len( other_scorers ) // 7 ) + 1

                # Keep track of total canucks and other scorers counter
                canucks_i = other_i = 0

                # Handle first box-score
                type = f'CANUCKS SCORER'
                # Iterate over CANUCKS SCORERS
                # Restrict first box-score to only go to 7
                for i in range( 0, min( len( canucks_scorers ), 7 ) ):
                    # Update CANUCKS SCORER
                    index = i + 3
                    text = make_scorer_text( canucks_scorers[ canucks_i ], 'CANUCKS' )
                    update_text( psxprj, index, text, type )

                    # Increment canucks scorers index
                    canucks_i += 1

                type = f'OTHER SCORER  '
                # Iterate over OTHER SCORERS
                # Restrict first box-score to only go to 7
                for i in range( 0, min( len( other_scorers ), 7 ) ):
                    # Update OTHER SCORER
                    index = i + 10
                    text = make_scorer_text( other_scorers[ other_i ], 'OTHER  ' )
                    update_text( psxprj, index, text, type )

                    # Increment other scorers index
                    other_i += 1

                # Update the source json
                with open( source + '/psxproject.json', 'w' ) as json_file:
                    json.dump( psxprj, json_file, indent=4 )
                    if ( DEBUG ):
                        print( f'''
        JSON File { source }/psxproject.json : Updated!
                        ''' )

                # Handle multiple box-scores if necessary
                if ( n > 1 ):
                    psx_path = cwd + '/assets/templates/box-score-temp/'
                    
                    # i = 2 because this will make box-score-2, box-score-3, ... box-score-n
                    for i in range( 2, n + 1 ):

                        destination = cwd + f'/json/games/{ date_file }/{ selected_choice }-temp-{ i }/'
                        copy_directory( psx_path, destination )
                        source = cwd + f'/json/games/{ date_file }/{ selected_choice }-temp-{ i }'

                        # Iterate over CANUCKS SCORERS
                        # Restrict box-score to only go to 7
                        start = canucks_i
                        for j in range( start, min( len( canucks_scorers ) - start, start + 7 ) ):
                            # Update CANUCKS SCORER
                            index = j - start + 3
                            text = make_scorer_text( canucks_scorers[ canucks_i ], 'CANUCKS' )
                            update_text( psxprj, index, text, type )

                            # Increment canucks scorers index
                            canucks_i += 1

                        # Iterate over OTHER SCORERS
                        # Restrict box-score to only go to 7
                        start = other_i 
                        for j in range( start, min( len( other_scorers ) - start, start + 7 ) ):
                            # Update OTHER SCORER
                    
                            index = j - start + 10
                            text = make_scorer_text( other_scorers[ other_i ], 'OTHER  ' )
                            update_text( psxprj, index, text, type )

                            # Increment other scorers index
                            other_i += 1

                        # Update the source json
                        with open( source + '/psxproject.json', 'w' ) as json_file:
                            json.dump( psxprj, json_file, indent=4 )
                            if ( DEBUG ):
                                print( f'''
                                JSON File { source }/psxproject.json : Updated!
                                ''' )
                        # Zip updated template
                        zip_directory( source, cwd + f'/json/games/{ date_file }/output/{ selected_choice }-{ i }.psxprj' )
                
                        print( f'''
                        Another { selected_choice } PSX file has been zipped to games/date/output/{ selected_choice }-{ i }.psxprj.
                        ''' )

                return True

    except Exception as e:
        print( f'''
        Update { type } : Failed
        { e }
        ''' )
        traceback.print_exc()
        return False
            
        
    # Update the source json
    with open( source + '/psxproject.json', 'w' ) as json_file:
        json.dump( psxprj, json_file, indent=4 )
        if ( DEBUG ):
            print( f'''
        JSON File { source }/psxproject.json : Updated!
            ''' )
    return True
    

def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser( description='Creates a PSX project of your choice for the Vancouver Canucks game today or a specified date.' )

    # Add argument for the choice
    parser.add_argument( '--choice', choices=[ 'game-day', 'final-score', 'box-score' ], help='Choose which type of PSX project to create.' )

    # Parse the command line arguments
    args = parser.parse_args()

    # Access the selected choice
    selected_choice = args.choice

    # Perform actions based on the selected choice
    if selected_choice not in [ 'game-day', 'final-score', 'box-score' ]:
        
        print( f'''
        Invalid choice: { selected_choice }. Please choose from the available options:
              game-day
              final-score
              box-score

        Use the format: python3 src/create-psx.py --choice game-day
        ''' )
        return
    
    print( f'''
############################################################
          
                CREATE { selected_choice.upper() } PSX FILE

############################################################
    ''' )
    # Get user input for a date
    date_file = input( '\nENTER DATE: ' )

    # Determine if date for game is valid
    accepted = 'ACCEPTED'
    if not date_file:
        date_file = datetime.today().strftime( '%b%d-%y' ).lower()
    else:
        date_file = date_file.lower()
        if not valid_date( date_file ):
            accepted = 'REJECTED\n\t\t\t\tACCEPTED FORMAT: jan09-24'

    print( f'''
############################################################
              
                DATE { date_file } { accepted }

############################################################
        ''' )
    if accepted != 'ACCEPTED':
        return
    
    # Find template path for selected choice
    psx_path = cwd + f'/assets/templates/{ selected_choice }-temp/'

    # Copy os-dependent psx project into template
    copy_file_to_directory( cwd + f'/assets/templates/{ os.sys.platform }/{ selected_choice }/psxproject.json', psx_path )

    # Create directory for game date and template if it doesn't exist
    destination = cwd + f'/json/games/{ date_file }/{ selected_choice }-temp/'
    create_directory( destination )

    # Copy selected template to new directory
    copy_directory( psx_path, destination )
    source = cwd + f'/json/games/{ date_file }/{ selected_choice }-temp'

    # Create output directory for PSX Files
    output = cwd + f'/json/games/{ date_file }/output'
    create_directory( output )

    # Update template copy
    if not update_psxprj( selected_choice, source, date_file ):
        return

    # Zip updated template
    zip_directory( source, cwd + f'/json/games/{ date_file }/output/{ selected_choice }.psxprj' )
    
    print( f'''
    A new { selected_choice } PSX file has been zipped to games/{ date_file }/output/{ selected_choice }.psxprj.
    ''' )
    return
    
    
if __name__ == '__main__':
    main()