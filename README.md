# [<kbd><img src='https://static.wixstatic.com/media/632f22_79a9ba856ef14ef88fd38405425d76c7~mv2.jpg/v1/fill/w_110,h_110,al_c,q_80,usm_0.66_1.00_0.01,enc_auto/Small%20Logo%202_edited.jpg' width='50' /></kbd>](https://www.nuckstalk.com/instagram-posts)PhotoScape Editor

PhotoScape Editor is a collection of scripts used by [nuckstalk.com](https://www.nuckstalk.com/instagram-posts) to automate the editing process of Canucks game Instagram posts. It streamlines tasks including game day previews, generating final score statistics, and summarizing box scores for social media posts.
<p align='center'><kbd><img src='/assets/screenshots/game-day-example.jpg' width='200' /></kbd><kbd><img src='/assets/screenshots/final-score-example.jpg' width='200' /></kbd><kbd><img src='/assets/screenshots/box-score-example.jpg' width='200' /></kbd></p>

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Design Decisions](#design-decisions)
- [License](#license)

## Installation

To install and set up the PhotoScape Editor, follow these steps:

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/llevasseur/photoscape-editor.git
    cd photoscape-editor
    ```
2. **Install Essential Components and Tools**
    - [PhotoScapeX](http://x.photoscape.org/)

    - [NodeJS](https://nodejs.org/en) (for Chocolatey)

    - [Python 3.11.x+](https://www.python.org/downloads/) (Make sure executable is called python3.exe on windows)

    - Make:
    ```bash
    # Install Make via Chocolatey
    choco install make
    ```
    - Pip
    ```bash
    # Install pip via Python
    python3 install pip
    ```
3. **Install Dependencies:**
    ```bash
    # Install selenium and any future requirements
    pip install -r requirements.txt
    ```

4. **Run the Scripts:**
    Execute the scripts to automate the editing process.
    ```bash
    # Example command
    make preview
    ```

## Usage

To use the PhotoScape Editor for automating Canucks game Instagram posts editing, follow these guidelines:

1. **Game Day Previews:**
    Run the following command to initialize a game day preview post.
    ```bash
    make preview
    ```

2. **Final Score Statistics:**
    Run the following command to initialize a final score statistics post.
    ```bash
    make final
    ```

3. **Box Score Summary:**
    Run the following command to initialize a box score summary post.
    ```bash
    make box
    ```
    
4. **Box Score Summary and Final Score Statistics:**
    Run the following command to initialize both a final score statistics post and a box score summary post.
    ```bash
    make final_full
    ```
   **Prompts**
   <p align='center'><kbd><img src='/assets/screenshots/url_example.jpg' width='320' /></kbd><kbd><img src='/assets/screenshots/date_example.jpg' width='290' /></kbd></p>

    - When prompt, enter a URL to a Canucks game from [ESPN](https://www.espn.com/nhl/game/_/gameId/401559812).


    - When prompt, enter a date in the form mmmDD-YY

        - "jan" represents the month abbreviation for January.
        - "DD" represents the day.
        - "YY" represents the last two digits of the year.

    **Output**
    - Find your output files in games/{date-entered}/output/{file}.psxprj.
    - Open the file with PhotoScape X.
    - Edit the file to see automated edits.

    <kbd>![Output for Game Day Preview](/assets/screenshots/photoscape-edit.jpg)</kbd>


## Design Decisions

PhotoScape Editor was designed with the following considerations:

1. **Ease of Use:**
    - This software is catered for non-technical creators at [nuckstalk.com](https://www.nuckstalk.com/instagram-posts).

2. **Idempotence**
    - This software can be ran at any point during a game to generate a "final" score or score "summary" even if the game hasn't concluded.
    - Previews can be made at any point.

3. **Scalability:**
    - Scripts can be used for any Canucks game that has a [ESPN](https://www.espn.com/nhl/game/_/gameId/401559812) website.

4. **Modularity:**
    - Scripts are reused based on input parameters.
    - Example: create-psx.py is reused for each post type.
    - Example: helper.py supplies functions to be reused by all python scripts.

## License

All Rights Reserved

This project is fully protected by copyright law and is the sole property of [nuckstalk.com](https://www.nuckstalk.com/instagram-posts). No part of this project may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the owner or developer, except in the case of brief quotations embodied in critical reviews and certain other noncommercial uses permitted by copyright law.

For permission requests, contact leevonlevasseur@gmail.com.

