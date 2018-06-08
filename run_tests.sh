#!/usr/bin/env bash
set -e
virtualenv venv --distribute
source venv/bin/activate
pip install googlemaps
PYTHONPATH=. python3 tests/calculations_tests.py