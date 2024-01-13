
import os
import shutil
import zipfile
import argparse
import re
import json
from datetime import datetime

cwd = os.getcwd()

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

def valid_date(s):
    try:
        return datetime.strptime(s, '%b%d-%y')
    except:
        msg = "Invalid date formate. Please use the format: jan09-24."
        raise argparse.ArgumentTypeError(msg)
    
def get_date_json(data, parsed_date):
    # Extract individual components
    month = parsed_date.strftime('%B')
    day = parsed_date.strftime('%d')
    year = parsed_date.year
    time = parsed_date.strftime('%I:%M %p').lstrip('0') # Time with AM/PM with no leading zeros
    date = f'{parsed_date.strftime("%b").lower()}{day}-{str(year)[-2:]}'

    day = parsed_date.day

    data["DATE"] = {
        "TIME": time,
        "MONTH": month,
        "DAY": day,
        "YEAR": year
    }
    
    return date

def extract_second_word(sentence):
    # Use regular expression to find the second word
    match = re.search(r'\b(?:[^\W\d_]+\b[^\W\d_]*){2}', sentence)

    if match:
        second_word = match.group().strip()
        return second_word
    else:
        return None
    
def remove_first_group(input_str):
    return re.sub(r'^\S+\s*', '', input_str, count=1)


def get_scorer_and_assistors(data, sentence, remove_nums):
    split_sentence = sentence.split('\n')
    
    data['SCORER'] = remove_first_group(split_sentence[0]).upper()
    
    # Determine if special goal type
    check_type = re.split(r'(.+?)\s*(\(\w+\s*\w*\))', data['SCORER'], maxsplit=1)
    print(check_type)       
    if check_type[3] != '':
        type = check_type[3].strip()
        with open(cwd + '/json/look-up/goal-type.json', 'r') as goal_types:
            special_goals = json.load(goal_types)
            match = re.search(r'\((.*?)\)', type)
            result = match.group(1) if match else ''

            type = special_goals.get(result.lower())

            data['TYPE'] = type

            data['SCORER'] = check_type[1] + ' ' + check_type[2]
            
    else:
        data['TYPE'] = ''

    if remove_nums:
        data['SCORER'] = re.sub(r' \(\d+\)', '', data['SCORER'])
        

    if split_sentence[1] == 'Unassisted':
        data['ASSISTORS'] = ['UNASSISTED']
    else:
        assists = split_sentence[1].split(', ')
        assists[0] = assists[0].replace('Assists: ', '')
        a = []
        for i in range(0, len(assists)):
            a.append(remove_first_group(assists[i]).upper())

            if remove_nums:
                a[i] = re.sub(r' \(\d+\)', '', a[i])

        data['ASSISTORS'] = a

    return