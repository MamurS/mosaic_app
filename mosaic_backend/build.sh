#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies from the root directory (one level up)
pip install -r ../requirements-prod.txt

# Run Django commands from the current directory ('insurance_project')
# where manage.py is located.
python manage.py collectstatic --no-input
python manage.py migrate