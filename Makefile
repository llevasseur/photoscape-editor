# Makefile

.PHONY: preview final box final_full

preview: run_game_day
final: run_final_score
box: run_box_score
final_full: run_final_full

run_game_day:
	python3 src/fetch-preview.py

run_final_score:
	python3 src/fetch-game-data.py --choice final-score

run_box_score:
	python3 src/fetch-game-data.py --choice box-score

run_final_full:
	python3 src/fetch-game-data.py --choice all
