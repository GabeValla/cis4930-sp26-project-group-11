#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Compile static files securely
python manage.py collectstatic --no-input

# Apply DB migrations
python manage.py migrate

# Seeding is skipped because the seeded db.sqlite3 is tracked in git!
