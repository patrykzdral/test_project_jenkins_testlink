#!/usr/bin/env bash
set -e
virtualenv venv --distribute -p python3
source venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. venv/bin/python tests/calculations_tests.py