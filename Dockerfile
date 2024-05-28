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

# Expose the port on which your Django app will run
EXPOSE 8000

# Command to run the server
CMD ["./start-server.sh"]
