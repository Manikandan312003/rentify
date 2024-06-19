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


# Add a script to wait for the DB to be ready before starting the server
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Add the start-server.sh script and make it executable
COPY start-server.sh /app/start-server.sh
RUN chmod +x /app/start-server.sh

# Expose the port on which your Django app will run
EXPOSE 8000

# Command to run the Django development server
CMD ["sh", "-c", "gunicorn Rentify.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
