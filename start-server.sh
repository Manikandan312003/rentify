#!/bin/sh

# Wait for PostgreSQL to be ready
/wait-for-it.sh $DATABASE_HOST:$DATABASE_PORT --timeout=60 --strict -- echo "PostgreSQL is up - executing command"

# Apply database migrations
python manage.py migrate

# Start the Django server
exec gunicorn Rentify.wsgi:application --bind 0.0.0.0:8000
