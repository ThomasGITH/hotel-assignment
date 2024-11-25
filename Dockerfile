FROM python:3.12.3-slim

# Sets environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc cron

# Installs pip and Django dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy  application code into the container
COPY . /app/

# Copy the .env file into the container (make sure it's included in the Docker build context)
COPY .env /app/

# Expose port 8000
EXPOSE 8000

# Run all commands necessary to run it
CMD ["bash", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py crontab add && python manage.py import_csv_data && python manage.py runserver 0.0.0.0:8000"]
