## Version 0.0.1
## create-psx.py

import os
import sys
import re
import zipfile
import json
import argparse

DEBUG = 1

def zip_file(file_to_zip, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as file:
        file.write(file_to_zip)
    

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
    if selected_choice == 'game-day':
        print(f'''
              You chose game-day.
        ''')
    elif selected_choice == 'final-score':
        print(f'''
              You chose final-score
        ''')
    elif selected_choice == 'box-score':
        print(f'''
              You chose box-score
        ''')
    else:
        print(f'''
        Invalid choice: {selected_choice}. Please choose from the available options:
              game-day
              final-score
              box-score
        Use the format: python3 create-psx.py --choice game-day
        ''')
        return

    #zip_file('example.txt', 'example.psxprj', )
    
    print(f'''
    A new {selected_choice} PSX file has been zipped to games/date/{selected_choice}.psxprj.
    ''')
    
    
if __name__ == "__main__":
    main()