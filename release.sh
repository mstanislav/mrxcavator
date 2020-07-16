#!/usr/bin/env bash

# Run `black` to check for formatting issues
black --line-length=80 mrxcavator.py

# Run `mypy` to check type annotations
mypy mrxcavator.py

# Run `flake8` to perform linting
flake8 mrxcavator.py

# Run `pdoc3` to update HTML documentation
pdoc3 --html -c show_source_code=False mrxcavator.py -o docs --force

# Run `poetry` to generate a requirements.txt file
poetry export -f requirements.txt > requirements.txt
