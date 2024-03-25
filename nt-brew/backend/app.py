"""
BUNDLE COMMANDS

python3 -m PyInstaller --onefile create-psx.py 
python3 -m PyInstaller --onefile --add-binary=./dist/create-psx:lib app.py

KILL PROCESS ON 5000
kill $(lsof -t -i:5000)
"""

import fetch_espn
import helpers as h
import multiprocessing
import os
import psutil
import pyautogui
import subprocess
import sys
import time

from flask import Flask, request, jsonify
from flask_cors import CORS
from signal import SIGKILL


error = "Undefined"

app = Flask(__name__)
CORS(app)  # enable cors for all origins

documents_folder = (
    os.path.join(os.environ["USERPROFILE"], "Documents")
    if os.name == "nt"
    else os.path.expanduser("~/Documents")
)

log_file_path = os.path.join(documents_folder, "NT", "logs", "electron.log")


def run_create_psx(choice):
    # Determine operating system to alter call to executable
    ext = ".exe" if os.name == "nt" else ""
    if h.running_from_executable():
        # path for create-psx.py when running from an executable
        script_path = os.path.join(sys._MEIPASS, f"lib/create-psx{ext}")
        command = [
            script_path,
            "--choice",
            choice,
        ]

    else:
        # path for create-psx.py when running from a .py script
        script_path = os.path.join(os.path.dirname(__file__), "create-psx.py")
        executable = sys.executable
        command = [
            executable,
            script_path,
            "--choice",
            choice,
        ]
    h.log_info(
        "app > run_create_psx",
        f"script_path: {script_path} Choice: {choice}, command: {command}",
        log_file_path,
    )

    # Run the create-psx executable
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    # Return the returncode, stdout, and stderr
    return process.returncode, stdout, stderr


# define a route /process-url that listens for POST requests
@app.route("/process-url", methods=["POST"])
def process_url():
    data = request.get_json()  # Extract JSON from the request
    if not data or "url" not in data:
        return jsonify(
            {"error": "Invalid request. Missing or malformed JSON data."}
        )
    h.log_info(
        "app > process_url",
        f"data: {data}",
        log_file_path,
    )
    url = data["url"]  # Extract the url field from the JSON Data
    selected_choice = data["choice"]
    date_file = "undefined"

    if selected_choice == "final-full" or selected_choice == "box-score":

        if not fetch_espn.fetch_box_score(url):

            # Stop loading
            os.environ["LOADING"] = "False"
            h.log_error(
                "app > process_url",
                600,
                f"Could not fetch box score. Error: {error}",
                log_file_path,
            )
            return (
                jsonify(
                    {
                        f"message": "Oh no! Could not fetch box score. Error: {error}"
                    }
                ),
                500,
            )

        else:

            # Run create-psx.py for box-score
            returncode, stdout, stderr = run_create_psx("box-score")

            # Check if the application ran successfully
            if returncode == 0:
                h.log_info(
                    "app > process_url",
                    f"create-psx on box score ran successfully. Output: {stdout.decode('utf-8')}",
                    log_file_path,
                )

                date_file = os.environ.get("FETCHED_DATE")

                h.log_info(
                    "app > process_url",
                    f"date_file: {date_file}",
                    log_file_path,
                )

            else:

                h.log_error(
                    "app > process_url",
                    601,
                    f"Error running create-psx in box score. Error message: {stderr.decode('utf-8')}",
                    log_file_path,
                )

    if selected_choice == "final-full" or selected_choice == "final-score":

        if not fetch_espn.fetch_final_score(url):

            # Stop loading
            os.environ["LOADING"] = "False"
            h.log_error(
                "app > process_url",
                602,
                f"Could not fetch final score. Error: {error}",
                log_file_path,
            )
            return (
                jsonify(
                    {
                        f"message": "Oh no! Could not fetch final score. Error: {error} "
                    }
                ),
                500,
            )

        else:

            # Run create-psx.py for final-score
            # Run create-psx.py for box-score
            returncode, stdout, stderr = run_create_psx("final-score")

            # Check if the application ran successfully
            if returncode == 0:
                h.log_info(
                    "app > process_url",
                    f"create-psx on final score ran successfully. Output: {stdout.decode('utf-8')}",
                    log_file_path,
                )

                date_file = os.environ.get("FETCHED_DATE")

                h.log_info(
                    "app > process_url",
                    f"date_file: {date_file}",
                    log_file_path,
                )

            else:
                h.log_error(
                    "app > process_url",
                    603,
                    f"Error running create-psx in final score. Error message: {stderr.decode('utf-8')}",
                    log_file_path,
                )

    if selected_choice == "game-day":

        if not fetch_espn.fetch_game_preview(url):

            # Stop loading
            os.environ["LOADING"] = "False"
            h.log_error(
                "app > process_url",
                604,
                f"Could not fetch game preview. Error: {error}",
                log_file_path,
            )
            return (
                jsonify(
                    {
                        f"message": "Oh no! Could not game preview. Error: {error} "
                    }
                ),
                500,
            )

        else:

            # Run create-psx.py for game-day
            # Run create-psx.py for box-score
            returncode, stdout, stderr = run_create_psx("game-day")

            # Check if the application ran successfully
            if returncode == 0:
                h.log_info(
                    "app > process_url",
                    f"create-psx on game day ran successfully. Output: {stdout.decode('utf-8')}",
                    log_file_path,
                )

                date_file = os.environ.get("FETCHED_DATE")

                h.log_info(
                    "app > process_url",
                    f"date_file: {date_file}",
                    log_file_path,
                )

            else:
                h.log_error(
                    "app > process_url",
                    605,
                    f"Error running create-psx in game day. Error message: {stderr.decode('utf-8')}",
                    log_file_path,
                )

    # Return message stating url received and pass the date_file
    # while( date_file == 'undefined'):
    #    date_file = os.environ.get('FETCHED_DATE')

    return jsonify({"date_file": date_file}), 200


def close_port( port: int ): 
    # TODO
    return
    for proc in psutil.process_iter():
        try:
            # Check if the process is a zombie
            if psutil.Process(proc.pid).status() == psutil.STATUS_ZOMBIE:
                continue # Skip zombie process

            for conns in proc.connections(kind='inet'):
                if conns.laddr.port == port:
                    proc.send_signal(SIGKILL) # or SIGKILL
                    h.log_info(
                        "app > close_port",
                        f"Port {port} closed!",
                        log_file_path,
                    )
                    time.sleep(3)
                    return
        except (psutil.NoSuchProcess, psutil.ZombieProcess):
            # Handle the case where the process no longer exists
            h.log_error(
                "app > close_port",
                606,
                f"Something went wrong!",
                log_file_path,
            )



if __name__ == "__main__":
    close_port(5000)
    app.run(debug=True)