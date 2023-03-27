"""All the general configuration of the project."""
from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

PAPER_DIR = SRC.joinpath("..", "..", "presentation_project_work").resolve()

__all__ = ["BLD", "SRC"]
