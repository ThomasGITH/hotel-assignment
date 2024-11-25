from django.shortcuts import render
from django.http import JsonResponse
from .models import City, Hotel
import json


def index(request):
    """
    Renders the index/main page of the application. The 
    list of cities is passed to it to be rendered.
    """

    cities = City.objects.all()
    return render(request, 'hotelapp/index.html', {'cities': cities})


def get_hotels(request, city_name):
    """
    Retrieves a list of hotels based on the
    name of a city.
    """

    try:
        city = City.objects.get(name=city_name)
        hotels = Hotel.objects.filter(city=city)
        hotel_data = list(hotels.values("id", "local_code", "name", "city"))
        return JsonResponse({"hotels": hotel_data})
    except City.DoesNotExist:
        return JsonResponse({"error": "City not found"}, status=404)


def manage_hotels(request):
    """
    Adds or updates the state of a hotel
    (i.e. 'managing') them. Since a hotel is 'unique' in that
    it has its own unique combination of a local_code and city,
    it will check whether such a hotel exists, and then try to
    update its name. If such a hotel does not exist, it will 
    create a new one with the passed city and local_code.
    """

    if request.method == "POST":
        data = json.loads(request.body)
        try:
            city = City.objects.get(code=data["city"])

            # Search wheter a hotel exists with this local code
            #  and city and put the result in 'hotel'
            hotelFiltered = Hotel.objects.filter(local_code=data["local_code"], city=data["city"])
            hotel_exists = hotelFiltered.exists()
            hotel = hotelFiltered.first()

            # If it exists, save it with its new name
            if hotel_exists:
                hotel.name = data["name"]
                hotel.save()
            else:
                # Otherwise, create a new hotel
                Hotel.objects.create(
                    name=data["name"], local_code=data["local_code"], city=city
                )
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def delete_hotel(request, hotel_id):
    """
    Endpoint that deletes a hotel
     with a given ID.
    """

    if request.method == "DELETE":
        try:
            hotel = Hotel.objects.get(pk=hotel_id)
            hotel.delete()
            return JsonResponse({"success": True})
        except Hotel.DoesNotExist:
            return JsonResponse({"error": "Hotel not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)
