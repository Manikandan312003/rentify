#!/bin/bash

# Log to a file
LOGFILE=/app/start-server.log

echo "Waiting for PostgreSQL to be ready..." | tee -a $LOGFILE
/wait-for-it.sh $DATABASE_HOST:$DATABASE_PORT --timeout=60 --strict -- echo "PostgreSQL is up - executing command" | tee -a $LOGFILE

echo "Applying database migrations..." | tee -a $LOGFILE
python manage.py migrate | tee -a $LOGFILE

echo "Starting the Django server..." | tee -a $LOGFILE
exec gunicorn Rentify.wsgi:application --bind 0.0.0.0:8000 | tee -a $LOGFILE
