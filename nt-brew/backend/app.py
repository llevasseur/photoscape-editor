import fetch_espn
import os
import subprocess

from flask import Flask, request, jsonify
from flask_cors import CORS

error = "Undefined"

app = Flask(__name__)
CORS(app)  # enable cors for all origins


def run_create_psx(choice):
    # path to the directory containing the create-psx executable
    create_psx_dir = os.path.join(os.path.dirname(__file__), "../../create-psx")

    # Determine operating system to alter call to executable
    ext = ".exe" if os.name == "nt" else ""

    # Command to run the create-psx app executable with the desired choice (game-day, final-score, box-score, final_full)
    command = [
        os.path.join(create_psx_dir, f"create-psx{ext}"),
        "--choice",
        choice,
    ]

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
    print(data)
    url = data["url"]  # Extract the url field from the JSON Data
    selected_choice = data["choice"]
    date_file = "undefined"

    if selected_choice == "final-full" or selected_choice == "box-score":

        if not fetch_espn.fetch_box_score(url):

            # Stop loading
            os.environ["LOADING"] = "False"
            print("Error!")
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
                print("create-psx ran successfully.")
                print("Output:")
                print(stdout.decode("utf-8"))

                date_file = os.environ.get("FETCHED_DATE")

                print(f'Date_file: {date_file}')

            else:
                print("Error running create-psx.")
                print("Error message:")
                print(stderr.decode("utf-8"))

    if selected_choice == "final-full" or selected_choice == "final-score":

        if not fetch_espn.fetch_final_score(url):

            # Stop loading
            os.environ["LOADING"] = "False"
            print("Error!")
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
                print("create-psx ran successfully.")
                print("Output:")
                print(stdout.decode("utf-8"))

                date_file = os.environ.get("FETCHED_DATE")

                print(f'Date_file: {date_file}')

            else:
                print("Error running create-psx.")
                print("Error message:")
                print(stderr.decode("utf-8"))

    if selected_choice == "game-day":

        if not fetch_espn.fetch_game_preview(url):

            # Stop loading
            os.environ["LOADING"] = "False"
            print("Error!")
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
                print("create-psx ran successfully.")
                print("Output:")
                print(stdout.decode("utf-8"))

                date_file = os.environ.get("FETCHED_DATE")

                print(f'Date_file: {date_file}')

            else:
                print("Error running create-psx.")
                print("Error message:")
                print(stderr.decode("utf-8"))

    # Return message stating url received and pass the date_file
    # while( date_file == 'undefined'):
    #    date_file = os.environ.get('FETCHED_DATE')

    return jsonify({"date_file": date_file}), 200


if __name__ == "__main__":
    print(fetch_espn)
    app.run(debug=True)
