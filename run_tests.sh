#!/usr/bin/env bash
set -e
virtualenv venv --distribute -p python3
source venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. venv/bin/python3 tests/calculations_tests.py
PYTHONPATH=. venv/bin/coverage run tests/calculations_tests.py
PYTHONPATH=. venv/bin/coverage report
PYTHONPATH=. venv/bin/coverage html
PYTHONPATH=. venv/bin/coverage xml
