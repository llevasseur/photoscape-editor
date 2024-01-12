## Version 0.0.1
## create-psx.py

import os
import sys
import shutil
import zipfile
import json
import argparse

cwd = os.getcwd()

DEBUG = 1

def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    return

def copy_directory(source_directory, destination_directory):
    if os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)
    shutil.copytree(source_directory, destination_directory)
    return

def zip_directory(directory_path, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                zipf.write(file_path, arcname=os.path.basename(file_path))
    return

def copy_file_to_directory(source_file, destination_directory):
    # Ensure that the destination directory exists
    os.makedirs(destination_directory, exist_ok=True)

    # Build the full path for the destination file
    destination_file = os.path.join(destination_directory, os.path.basename(source_file))

    # Copy the file to the destination directory
    shutil.copy(source_file, destination_file)

    return

def update_logo(source, psxprj, i, logo_path, type):
    # Copy logo into source
    copy_file_to_directory(logo_path, source)
    
    destination_file = os.path.basename(logo_path)

    # Reference logo basename in psxprj object
    psxprj.get('object')['_v'][i]['_v']['image']['_v']['_v'] = destination_file
    
    if (DEBUG):
        print(f'''
        Update {type} : Complete
        ''')
    return

def update_text(psxprj, i, text, type):
    # Reference new text in psxprj object
    psxprj.get('object')['_v'][i]['_v']['text']['_v'] = text
    
    if (DEBUG):
        print(f'''
        Update {type} : Complete
        ''')
    return


def update_psxprj(selected_choice, source, date_file):
    # Find psxprj from copied template source json
    with open(source + '/psxproject.json', 'r') as json_file:
        psxprj = json.load(json_file)
        
    # Get team logo data from team look-up json
    with open(cwd + '/json/look-up/teams.json', 'r') as logo_file:
        team_lookup = json.load(logo_file)

    # Get selected choice data from related json
    with open(cwd + f'/json/games/{date_file}/{selected_choice}.json', 'r') as stats_file:
        stats = json.load(stats_file)

    match selected_choice:
        case 'game-day':
            try:
                # Update VAN LOGO
                type = 'VAN Logo'
                index = 0
                #NOTE Change IMG to ALT1, ALT2, ALT3
                logo = team_lookup.get('VAN')['IMG']
                update_logo(source, psxprj, index, logo, type)

                # Update OTHER LOGO
                other = stats.get('OTHER')['TEAM']
                type = f'{other} Logo'
                index = 1
                logo = team_lookup.get(stats.get('OTHER')['TEAM'])['IMG']
                update_logo(source, psxprj, index, logo, type)

                # Update TIME
                type = 'Time'
                index = 9
                time = stats.get('DATE')['TIME']
                update_text(psxprj, index, time, type)

                # Update DATE
                type = 'Date'
                index = 10
                date = f'{stats.get("DATE")["MONTH"]} {stats.get("DATE")["DAY"]}, {stats.get("DATE")["YEAR"]}'
                update_text(psxprj, index, date, type)

                # Update VAN RECORD
                type = 'VAN Record'
                index = 13
                record = stats.get('CANUCKS')['RECORD']
                update_text(psxprj, index, record, type)

                # Update OTHER RECORD
                type = f'{other} Record'
                index = 14
                record = stats.get('OTHER')['RECORD']
                update_text(psxprj, index, record, type)

                # Update HOME or AWAY
                type = 'HOME or AWAY'
                index = 16
                where = 'HOME' if stats.get('CANUCKS')['HOME'] == 'True' else 'AWAY'
                update_text(psxprj, index, where, type)
            
            except Exception as e:
                print(f'''
                Update {type} : Failed
                {e}
                ''')
                return False
        
        case 'final-score':
            try:
                # Update VAN LOGO
                type = 'VAN Logo'
                index = 0
                #NOTE Change IMG to ALT1, ALT2, ALT3
                logo = team_lookup.get('VAN')['IMG']
                update_logo(source, psxprj, index, logo, type)

                # Update OTHER LOGO
                # TODO Make a function
                other = stats.get('OTHER')['TEAM']
                type = f'{other} Logo'
                index = 1
                logo = team_lookup.get(stats.get('OTHER')['TEAM'])['IMG']
                update_logo(source, psxprj, index, logo, type)

                # Update VAN SCORE
                type = 'VAN Score'
                index = 11
                score = stats.get('CANUCKS')['SCORE']
                update_text(psxprj, index, score, type)

                # Update OTHER SCORE
                type = f'{other} Score'
                index = 12
                score = stats.get('OTHER')['SCORE']
                update_text(psxprj, index, score, type)

                # Update VAN SOG
                type = 'VAN SOG'
                index = 20
                sog = stats.get('CANUCKS')['SOG']
                update_text(psxprj, index, sog, type)

                # Update VAN HITS
                type = 'VAN HITS'
                index = 21
                hits = stats.get('CANUCKS')['HITS']
                update_text(psxprj, index, hits, type)

                # Update VAN PP
                type = 'VAN PP'
                index = 22
                pp = stats.get('CANUCKS')['PP']
                update_text(psxprj, index, pp, type)

                # Update VAN PIM
                type = 'VAN PIM'
                index = 23
                pim = stats.get('CANUCKS')['PIM']
                update_text(psxprj, index, pim, type)

                # Update VAN FO
                type = 'VAN FO'
                index = 24
                fo = stats.get('CANUCKS')['FO']
                update_text(psxprj, index, fo, type)

                # Update OTHER SOG
                type = f'{other} SOG'
                index = 25
                sog = stats.get('OTHER')['SOG']
                update_text(psxprj, index, sog, type)

                # Update OTHER HITS
                type = f'{other} HITS'
                index = 26
                hits = stats.get('OTHER')['HITS']
                update_text(psxprj, index, hits, type)

                # Update OTHER PP
                type = f'{other} PP'
                index = 27
                pp = stats.get('OTHER')['PP']
                update_text(psxprj, index, pp, type)

                # Update OTHER PIM
                type = f'{other} PIM'
                index = 28
                pim = stats.get('OTHER')['PIM']
                update_text(psxprj, index, pim, type)

                # Update OTHER FO
                type = f'{other} FO'
                index = 29
                fo = stats.get('OTHER')['FO']
                update_text(psxprj, index, fo, type)

                # Update DATE
                type = 'Date'
                index = 30
                date = f'{stats.get("DATE")["MONTH"]} {stats.get("DATE")["DAY"]}, {stats.get("DATE")["YEAR"]}'
                update_text(psxprj, index, date, type)

                # Update HOME or AWAY
                type = 'HOME or AWAY'
                index = 31
                where = 'HOME' if stats.get('CANUCKS')['HOME'] == 'True' else 'AWAY'
                update_text(psxprj, index, where, type)

                # Update WIN or LOSS
                type = 'WIN or LOSS'
                index = 33
                win = 'WIN' if stats.get('CANUCKS')['WIN'] == 'True' else 'LOSS'
                if stats.get('CANUCKS')['OT'] == 'True':
                    if stats.get('CANUCKS')['SO'] == 'True':
                        win += ' (SO)'
                    else:
                        win += ' (OT)'
                update_text(psxprj, index, win, type)

            except Exception as e:
                print(f'''
                Update {type} : Failed
                {e}
                ''')
                return False
        
        case 'box-score':
            print("hit box-score")
            return
        
    # Update the source json
    with open(source + '/psxproject.json', 'w') as json_file:
        json.dump(psxprj, json_file, indent=4)
        if (DEBUG):
            print(f'''
            JSON File : Updated!
            ''')
    return True
    

def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Creates a PSX project of your choice for the Vancouver Canucks game.')

    # Add argument for the choice
    parser.add_argument('--choice', choices=['game-day', 'final-score', 'box-score'], help='Choose which type of PSX project to create.')

    # Parse the command line arguments
    args = parser.parse_args()

    # Access the selected choice
    selected_choice = args.choice

    # Perform actions based on the selected choice
    if selected_choice not in ['game-day', 'final-score', 'box-score']:
        
        print(f'''
        Invalid choice: {selected_choice}. Please choose from the available options:
              game-day
              final-score
              box-score

        Use the format: python3 src/create-psx.py --choice game-day
        ''')
        return
    
    # Find template path for selected choice
    with open(cwd + '/json/look-up/psx-files.json', 'r') as json_file:
        psx_type = json.load(json_file).get(selected_choice)
        psx_path = cwd + psx_type['PATH']
        
    print(f'''
    Selected file path is {psx_path}
    ''')

    # Determine date for game
    # TODO
    date_file = 'jan9-24'
    
    # Create directory for game date and template if it doesn't exist
    destination = cwd + f'/json/games/{date_file}/{selected_choice}-temp/'
    create_directory(destination)

    # Copy selected template to new directory
    copy_directory(psx_path, destination)
    source = cwd + f'/json/games/{date_file}/{selected_choice}-temp'

    # Update template copy
    if not update_psxprj(selected_choice, source, date_file):
        return

    # Zip updated template
    zip_directory(source, cwd + f'/json/games/{date_file}/{selected_choice}.psxprj')
    
    print(f'''
    A new {selected_choice} PSX file has been zipped to games/date/{selected_choice}.psxprj.
    ''')
    return
    
    
if __name__ == '__main__':
    main()