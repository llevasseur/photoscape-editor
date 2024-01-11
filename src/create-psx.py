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

def copy_directory(source_directory, destination_directory):
    if os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)
    shutil.copytree(source_directory, destination_directory)

def zip_directory(directory_path, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                zipf.write(file_path, arcname=os.path.basename(file_path))
    

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
    # TODO

    # Zip updated template
    zip_directory(source, cwd + f'/json/games/{date}/{selected_choice}.psxprj')
    
    print(f'''
    A new {selected_choice} PSX file has been zipped to games/date/{selected_choice}.psxprj.
    ''')
    
    
if __name__ == "__main__":
    main()