# Makefile

.PHONY: preview final

preview: run_game_day
final: run_final_score run_box_score

run_game_day:
	python3 src/create-psx.py --choice game-day

run_final_score:
	python3 src/create-psx.py --choice final-score

run_box_score:
	python3 src/create-psx.py --choice box-score