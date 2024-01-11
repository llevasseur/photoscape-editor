# photoscape-editor
A project devoted to automating game score updates for social media posts, particularly for sports using PhotoScape X.

## Initial Thoughts
**Input:** template.psxprj, url for sports stats
**Output:** jpg

Will need two projects that work together.
1. ESPN Stat Scrapper
 - Take url and determine relevant stats.
 - Save as json.

#### Info Needed
 - Who the two teams are
 - Is vancouver Home or Away
 - Final score between the two teams - INT(2)
 - Did van win, was it in ot or shootout?
 - Shots on goal for both teams - INT(3)
 - Hits for both teams - INT(3)
 - Powerplay fraction for both teams - STRING(5)
 - Faceoff wins for both teams - INT(3)
 - Date played
 
 - For each Canucks goal:
 - Last name of goal scorer, their total goal number, which period, and at what time in the period.
 - Last name of primary assistor, their total assists.
 - Last name of secondary assistor, their total assists.

------------------------------------------------------
2. PhotoScape Editor
 - Unzip template input json format.
 - Alter json file and zip file as psxprj or jpg.

#### Final Score
 - Canucks Logo
 - Opposition Logo - Need to request from Kyle
 - Final Score between the two teams
 - Shots on goal for both teams
 - Hits for both teams
 - Powerplay fraction for both teams
 - Faceoff wins for both teams
 - Win or Lose
 - Date in form MMM DD, YYYY, could be D


#### Box Score
 - Column list of Goal information, left is always Canucks.
 - Period - (Time Scored)
 - G: Last name of goal scorer (# of goals)
 - A: Last name of primary assistor (# of assists)(optional), last name of secondary assistor (# of assists)(optional)

 - On the other side:
 - (Time Scored) - Period
 - Last name of goal scorer :G
 - Last name of primary assistor (optional), last name of secondary assistor (optional) :A

 #### Unzip Process
 1. Take .psxprj file and unzip it into a folder called unzip
 2. Edit psxproject.json as required

 #### Zip Process
 1. In unzip/ recursively zip all files into {DATE}.psxprj
 2. Open the file in Photoscape X, click edit
 3. Save file as a jpg.

-------------------------------------------------------
#### PhotoScape Notes
Note that z-index matters in photoscape json files. This means objects at the bottom of the json appear on top of objects above them.

Note you must change the name of the logo pngs in the json and the template.

Note automatically updating text seems to make it appear smaller than it did before. Update the font sizes accordingly in the templates.

#### Other
Maybe I should keep a small database for canucks players' stats. That would be useful to get total goals and total assists for players. Also would be interesting to track stats in general about those players as it caters to our audience.

Format: JSON
ESPN Data:
 - G
 - A
 - +/-
 - S 

## Installation
[Todo]

## Usage
[Todo]

## Design Decisions
[Todo]

## License
This project is private for now and licensed under [MIT License](https://opensource.org/licenses/MIT).

