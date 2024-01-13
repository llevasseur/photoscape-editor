
import os
import shutil
import zipfile
import argparse
from datetime import datetime

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