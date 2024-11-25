from django.test import TestCase
from django.urls import reverse
from .models import City, Hotel
import json


class HotelViewTests(TestCase):
    """
    Testing class for some common hotel-related actions that
    can be performed with the endpoints.
    """

    def setUp(self):
        """
        Set up some test data for cities and hotels.
        """

        # Create cities
        self.city1 = City.objects.create(name="Antwerpen", code="ANT")
        self.city2 = City.objects.create(name="Brussel", code="BRU")

        # Create hotels
        self.hotel1 = Hotel.objects.create(name="Hotel 1", local_code="ANT01", city=self.city1)
        self.hotel2 = Hotel.objects.create(name="Hotel 2", local_code="ANT02", city=self.city1)

        # URL for hotel-related endpoints
        self.get_hotels_url = reverse('get_hotels', args=[self.city1.name])
        self.manage_hotels_url = reverse('manage_hotels')
        self.delete_hotel_url = reverse('delete_hotel', args=[self.hotel1.id])

    def test_get_hotels(self):
        """
        Test retrieving hotels for an existing city.
        """

        # Send GET request to fetch hotels for city1
        response = self.client.get(self.get_hotels_url)
        
        # Assert status is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Assert the response contains the expected hotel data
        response_data = response.json()
        self.assertIn('hotels', response_data)
        self.assertEqual(len(response_data['hotels']), 2)
        self.assertEqual(response_data['hotels'][0]['name'], "Hotel 1")
        self.assertEqual(response_data['hotels'][1]['name'], "Hotel 2")

    def test_get_hotels_city_not_found(self):
        """
        Test fetching hotels for a non-existent city.
        """

        # Send GET request for a non-existent city
        response = self.client.get(reverse('get_hotels', args=["NonExistentCity"]))
        
        # Assert status is 404 (Not Found)
        self.assertEqual(response.status_code, 404)
        
        # Assert error message
        response_data = response.json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], "City not found")

    def test_manage_hotels_create(self):
        """
        Test creating a new hotel.
        """

        new_hotel_data = {
            "name": "Hotel 3",
            "local_code": "ANT03",
            "city": self.city1.code
        }
        
        # Send POST request to create a new hotel
        response = self.client.post(self.manage_hotels_url,
         data=json.dumps(new_hotel_data), content_type='application/json')
        
        # Assert the hotel was created successfully
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json())
        
        # Assert the hotel was actually created in the database
        hotel = Hotel.objects.get(local_code="ANT03")
        self.assertEqual(hotel.name, "Hotel 3")
        self.assertEqual(hotel.city, self.city1)

    def test_manage_hotels_update(self):
        """
        Test updating an existing hotel.
        """

        update_data = {
            "name": "Updated Hotel 1",
            "local_code": self.hotel1.local_code,
            "city": self.city1.code
        }

        # Send POST request to update the hotel
        response = self.client.post(self.manage_hotels_url, 
        data=json.dumps(update_data), content_type='application/json')
        
        # Assert the update was successful
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json())
        
        # Assert the hotel name was updated
        self.hotel1.refresh_from_db()
        self.assertEqual(self.hotel1.name, "Updated Hotel 1")

    def test_manage_hotels_invalid_method(self):
        """
        Test sending a request with invalid method to the manage hotels endpoint.
        """

        # Purposely use GET instead of POST
        response = self.client.get(self.manage_hotels_url)

        # Correct response would be 'Method Not Allowed'
        self.assertEqual(response.status_code, 405)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Invalid request method')

    def test_delete_hotel(self):
        """
        Test deleting an existing hotel.
        """

        # Send DELETE request to delete the hotel
        response = self.client.delete(self.delete_hotel_url)
        
        # Assert the deletion was successful
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json())
        
        # Assert the hotel is no longer in the database
        with self.assertRaises(Hotel.DoesNotExist):
            Hotel.objects.get(pk=self.hotel1.id)

    def test_delete_hotel_not_found(self):
        """
        Test deleting a hotel that doesn't exist.
        """

        # Send DELETE request for a non-existent hotel ID
        response = self.client.delete(reverse('delete_hotel', args=[999999]))
        
        # Assert the response is a 404 error
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], "Hotel not found")

    def test_delete_hotel_invalid_method(self):
        """
        Test using an invalid method for the delete hotel endpoint.
        """

        # Purposely using POST instead of DELETE
        response = self.client.post(self.delete_hotel_url)

        # Correct response would be 'Method Not Allowed'
        self.assertEqual(response.status_code, 405)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Invalid request method')
