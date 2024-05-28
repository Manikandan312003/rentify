# Use the official Python image as base
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code into the container
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Command to run the server
CMD sh -c 'echo "Waiting for PostgreSQL to be ready..." && /wait-for-it.sh $DATABASE_HOST:$DATABASE_PORT --timeout=60 --strict && echo "PostgreSQL is up - executing command" && python manage.py migrate && echo "Applying database migrations..." && exec gunicorn Rentify.wsgi:application --bind 0.0.0.0:8000'
