from django.contrib import admin
from .models import City
from .models import Hotel

# Registers the 'hotel' and 'city' objects
# to the admin dashboard
admin.site.register(City)
admin.site.register(Hotel)