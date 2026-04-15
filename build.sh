#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Compile static files securely
python manage.py collectstatic --no-input

# Apply DB migrations into Postgres
python manage.py migrate

# Seed baseline data
python manage.py seed_data --limit 10000
python manage.py fetch_data
