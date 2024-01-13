# Makefile

.PHONY: preview final box

preview: run_game_day
final: run_final_score
box: run_box_score

run_game_day:
	python3 src/create-psx.py --choice game-day --date jan09-24

run_final_score:
	python3 src/create-psx.py --choice final-score --date jan09-24

run_box_score:
	python3 src/create-psx.py --choice box-score --date jan09-24