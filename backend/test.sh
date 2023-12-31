#! /usr/bin/env bash
set -e

alembic upgrade head

python app/initial_data.py

pytest --cov=app --cov-report=term-missing --junitxml=report.xml app/tests
