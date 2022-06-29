# __init__.py

"""Boxfish, a lightweight tool for table extraction from HTML pages."""

import pathlib

from . import data

# Main modules
from data import config
from data import soups
from data import website

# Main functions
from data.config import build, create
from data.website import extract

# Version
__version__ = (pathlib.Path(__file__).parent / "VERSION").read_text()

# Initialization
print('Initializing boxfish ...')
