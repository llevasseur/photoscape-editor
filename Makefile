# Makefile

.PHONY: preview final box final_full

preview: run_fetch_preview run_game_day
final: run_fetch_game_data run_final_score
box: run_fetch_game_data run_box_score

final_full: run_fetch_game_data run_final_score run_box_score


run_fetch_preview:
	python3 src/fetch-preview.py

run_fetch_game_data:
	python3 src/fetch-game-data.py

run_game_day:
	python3 src/create-psx.py --choice game-day

run_final_score:
	python3 src/create-psx.py --choice final-score

run_box_score:
	python3 src/create-psx.py --choice box-score