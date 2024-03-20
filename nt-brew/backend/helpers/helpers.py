import argparse
import json
import os
import re
import shutil
import sys
import time
import zipfile

from datetime import datetime

cwd = os.path.join(os.path.dirname(__file__))

documents_folder = (
    os.path.join(os.environ["USERPROFILE"], "Documents")
    if os.name == "nt"
    else os.path.expanduser("~/Documents")
)

log_file_path = os.path.join(documents_folder, "NT", "logs", "electron.log")


def log_to_file(log_file_path, message):
    timestamp = datetime.now().isoformat()
    log_message = f"{timestamp}: {message}\n"
    with open(log_file_path, "a") as file:
        file.write(log_message)


def log_error(module, error_code, message, log_file_path):
    formatted_message = f"[ERROR][{module}][{error_code}] {message}"
    print(formatted_message, file=sys.stderr)
    log_to_file(log_file_path, formatted_message)


def log_info(module, message, log_file_path):
    formatted_message = f"[INFO][{module}] {message}"
    print(formatted_message)
    log_to_file(log_file_path, formatted_message)


def log_warning(module, message, log_file_path):
    formatted_message = f"[WARNING][{module}] {message}"
    print(formatted_message)
    log_to_file(log_file_path, formatted_message)


def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    return


def copy_directory(source_directory, destination_directory):
    log_info(
        "helpers > copy_directory",
        f"source {source_directory} dest: {destination_directory}",
        log_file_path,
    )
    if os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)
    shutil.copytree(source_directory, destination_directory)
    return


def zip_directory(directory_path, zip_name):
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                zipf.write(file_path, arcname=os.path.basename(file_path))
    return


def copy_file_to_directory(source_file, destination_directory):
    # Ensure that the destination directory exists
    os.makedirs(destination_directory, exist_ok=True)

    # Build the full path for the destination file
    destination_file = os.path.join(
        destination_directory, os.path.basename(source_file)
    )

    # Copy the file to the destination directory
    shutil.copy(source_file, destination_file)

    return


def valid_date(s):
    try:
        return datetime.strptime(s, "%b%d-%y")
    except:
        msg = "Invalid date formate. Please use the format: jan09-24."
        raise argparse.ArgumentTypeError(msg)


def get_date_json(data, parsed_date):
    # Extract individual components
    month = parsed_date.strftime("%B")
    day = parsed_date.strftime("%d")
    year = str(parsed_date.year)
    time = parsed_date.strftime("%I:%M %p").lstrip(
        "0"
    )  # Time with AM/PM with no leading zeros
    date = f'{ parsed_date.strftime( "%b" ).lower() }{ day }-{ str( year )[ -2: ] }'

    day = str(parsed_date.day)

    data["DATE"] = {"TIME": time, "MONTH": month, "DAY": day, "YEAR": year}

    return date


def extract_second_word(input_str):
    # Use regular expression to find the second word
    match = re.findall(r"\S+", input_str)

    if match:
        return match[1]
    else:
        return ""


def loading_animation():

    loading_speed = 4  # number of characters to print out per second
    loading_string = (
        "." * 6
    )  # characters to print out one by one (6 dots in this example)
    log_info("helpers loading_animation", "Collecting pucks", log_file_path)
    sys.stdout.write("Collecting pucks")
    while os.environ.get("LOADING") == "True":

        for index, char in enumerate(loading_string):
            if os.environ.get("LOADING") != "True":
                break
            sys.stdout.write(char)  # write the next char to STDOUT
            sys.stdout.flush()  # flush the output
            time.sleep(1.0 / loading_speed)  # wait to match our speed

        index += 1  # lists are zero indexed, we need to increase by one for the accurate count
        # backtrack the written characters, overwrite them with space, backtrack again:
        sys.stdout.write("\b" * index + " " * index + "\b" * index)
        sys.stdout.flush()  # flush the output


def remove_first_group(input_str):
    return re.sub(r"^\S+\s*", "", input_str, count=1)


def get_scorer_and_assistors(data, input_str, remove_nums):

    goal_types = {
        "power play": "PP",
        "shorthanded": "SH",
        "empty net": "EN",
        "penalty shot": "PS",
    }

    split_input_str = input_str.split("\n")

    data["SCORER"] = remove_first_group(split_input_str[0]).upper()

    # Determine if special goal type
    check_type = re.split(
        r"(.+?)\s*(\(\w+\s*\w*\))", data["SCORER"], maxsplit=1
    )
    if len(check_type) > 3 and check_type[3] != "":
        type = check_type[3].strip()
        match = re.search(r"\((.*?)\)", type)
        result = match.group(1) if match else ""

        type = goal_types.get(result.lower())

        data["TYPE"] = type

        data["SCORER"] = check_type[1] + " " + check_type[2]

    else:
        data["TYPE"] = ""

    if remove_nums:
        data["SCORER"] = re.sub(r"\(\d+\)", "", data["SCORER"]).strip()

    if split_input_str[1] == "Unassisted":
        data["ASSISTORS"] = ["UNASSISTED"]
    else:
        assists = split_input_str[1].split(", ")
        assists[0] = assists[0].replace("Assists: ", "")
        a = []
        for i in range(0, len(assists)):
            a.append(remove_first_group(assists[i]).upper().strip())

            if remove_nums:
                a[i] = re.sub(r"\(\d+\)", "", a[i]).strip()

        data["ASSISTORS"] = a

    return


def running_from_executable():
    # check if the script is frozen (compiled into an executable)
    if getattr(sys, "frozen", False):
        return True
    # If running from a script, it's not frozen
    return False
