## Version 0.0.1
## create-psx.py

import os
import sys
import re
import zipfile

DEBUG = 1

def zip_file(file_to_zip, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as file:
        file.write(file_to_zip)
    

def main():
    zip_file('example.txt', 'example.psxprj', )
    
    print('''
    File example.txt has been zipped to example.zip.
    ''')
    
    
if __name__ == "__main__":
    main()