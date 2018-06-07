#!/usr/bin/env bash
set -e

source venv/bin/activate

PYTHONPATH=. python tests/calculations_tests.py