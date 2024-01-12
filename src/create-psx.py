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
    os.makedirs(destination_directory, exists_ok=True)

    # Build the full path for the destination file
    destination_file = os.path.join(destination_directory, os.path.basename(source_file))

    # Copy the file to the destination directory
    shutil.copy(source_file, destination_file)

    return

def update_logo(source, object, logo_path, type):
    # Copy logo into source
    copy_file_to_directory(logo_path, source)
    destination_file = os.path.basename(logo_path)

    # Reference logo basename in object
    object = destination_file
    
    if (DEBUG):
        print(f'''
        Update {type} : Complete
        ''')
    return

def update_text(object, text, type):
    object = text
    if (DEBUG):
        print(f'''
        Update {type} : Complete
        ''')
    return


def update_psxprj(selected_choice, source):
    # Find psxprj from source
    with open(source + '/psxproject.json', 'r') as json_file:
        psxprj = json.load(json_file)
        
    with open(cwd + '/json/look-up/teams.json', 'r') as logo_file:
        team_lookup = json.load(logo_file)

    match selected_choice:
        case "game-day":
            try:
                # Update VAN LOGO
                type = "VAN Logo"
                object = psxprj.get('object')['_v'][0]['_v']['image']['_v']['_v']
                logo = team_lookup.get('VAN')['IMG']
                update_logo(object, logo, type)

                # Update OTHER LOGO
                type = "OTHER Logo"
                object = psxprj.get('object')['_v'][1]['_v']['image']['_v']['_v']
                logo = team_lookup.get('NYI')['IMG']
                update_logo(object, logo, type)

                # Update TIME
                type = "Time"
                object = psxprj.get('object')['_v'][9]['_v']['text']['_v']
                time = "4:00 PM"
                update_text(object, time, type)

                # Update DATE
                type = "Date"
                object = psxprj.get('object')['_v'][10]['_v']['text']['_v']
                date = "January 9, 2024"
                update_text(object, date, type)

                # Update VAN RECORD
                type = "VAN Record"
                object = psxprj.get('object')['_v'][13]['_v']['text']['_v']
                record = "27-11-3"
                update_text(object, record, type)

                # Update OTHER RECORD
                type = "OTHER Record"
                object = psxprj.get('object')['_v'][14]['_v']['text']['_v']
                record = "13-16-5"
                update_text(object, record, type)

                # Update HOME or AWAY
                type = "HOME or AWAY"
                object = psxprj.get('object')['_v'][16]['_v']['text']['_v']
                where = "HOME"
                update_text(object, where, type)
            
            except:
                print(f'''
                Update {type} : Failed
                ''')
                return False
            
            # Update the source json
            with open(source + '/psxproject.json', 'w') as json_file:
                json.dump(psxprj, json_file, indent=4)

            return True
        
        case "final-score":
            return
        
        case "box-score":
            return
    

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
    date = 'jan9-24'
    
    # Create directory for game date and template if it doesn't exist
    destination = cwd + f'/json/games/{date}/{selected_choice}-temp/'
    create_directory(destination)

    # Copy selected template to new directory
    copy_directory(psx_path, destination)
    source = cwd + f'/json/games/{date}/{selected_choice}-temp'

    # Update template copy
    if not update_psxprj(selected_choice, source):
        return

    # Zip updated template
    zip_directory(source, cwd + f'/json/games/{date}/{selected_choice}.psxprj')
    
    print(f'''
    A new {selected_choice} PSX file has been zipped to games/date/{selected_choice}.psxprj.
    ''')
    return
    
    
if __name__ == "__main__":
    main()