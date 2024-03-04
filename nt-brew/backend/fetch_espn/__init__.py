# This file is not strictly required to declare a package but
# it still serves as important. It marks the directory as a Python 
# package so that it can import modules and subpackages from it. Use 
# this file as necessary to define variable, import modules, or execute
# code that needs to be run when the package is imported. Control what
# gets imported when this package is imported. This is done be by
# specifying the `__all__` variable. Lastly, contain namespace declarations
# or other package-wide definitions that you want to be available.

from .fetch_espn import fetch_game_preview, fetch_box_score, fetch_final_score