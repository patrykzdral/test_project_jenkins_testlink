#!/usr/bin/env bash
set -e

source venv/bin/activate

PYTHONPATH=. python3.6 tests/calculations_tests.py