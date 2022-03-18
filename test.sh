#! /usr/bin/env bash
set PYTHONPATH=.
alembic upgrade head
python app/initial_data.py
pytest --cov=app --cov-report=term-missing app/tests
