"""Run the complete project pipeline from the repository root."""

from src.prepare_data import main as prepare_data
from src.run_analysis import main as run_analysis
from src.make_visuals import main as make_visuals


if __name__ == "__main__":
    prepare_data()
    run_analysis()
    make_visuals()
