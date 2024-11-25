import os
import csv
import requests
from django.core.management.base import BaseCommand
from hotelapp.models import City, Hotel

"""
This file defines a Django-command that will import city and 
hotel CSV data (in an expected format) from two URL's saved 
in environment variables.
"""

# CSV data URLs
CITY_CSV_URL = os.getenv("CITY_CSV_URL")
HOTEL_CSV_URL = os.getenv("HOTEL_CSV_URL")

# HTTP Authentication info
AUTH_INFO = (os.getenv("AUTH_USERNAME"),
             os.getenv("AUTH_PASSWORD"))


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.import_cities()
        self.import_hotels()

    def import_cities(self):
        response = requests.get(CITY_CSV_URL, auth=AUTH_INFO)

        # Makes sure to give an error if one occured
        response.raise_for_status()

        csv_content = response.text.splitlines()
        reader = csv.reader(csv_content, delimiter=";")

        for row in reader:
            code, name = row
            City.objects.update_or_create(
                code=code, defaults={"name": name})

        # Note that this line probably won't work when 
        # performed by the cronjob. In a real project I 
        # would use logging for this.
        self.stdout.write(self.style.SUCCESS("Done importing cities"))

    def import_hotels(self):
        response = requests.get(HOTEL_CSV_URL, auth=AUTH_INFO)
        response.raise_for_status()

        csv_content = response.text.splitlines()
        reader = csv.reader(csv_content, delimiter=";")

        for row in reader:
            city_code, full_hotel_code, name = row

            # Extract the local hotel code. These are
            # the last two symbols.
            local_code = full_hotel_code[-2:]
            city = City.objects.get(code=city_code)

            # Does the combination (i.e. composite key) of city and
            # local_code exist? Update it. Otherwise create it.
            Hotel.objects.update_or_create(
                local_code=local_code, city=city, defaults={"name": name})

        # Note that this line probably won't work when z
        # performed by the cronjob. In a real project I 
        # would use logging for this.
        self.stdout.write(self.style.SUCCESS("Done importing hotels"))
