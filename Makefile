.PHONY: all prepare analyze visuals

all:
	python run_all.py

prepare:
	python src/prepare_data.py

analyze:
	python src/run_analysis.py

visuals:
	python src/make_visuals.py
