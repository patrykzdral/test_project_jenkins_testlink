#!/usr/bin/env bash
set -e
source venv/bin/activate
PYTHONPATH=. python3 tests/calculations_tests.py