from django.urls import path

from . import views

urlpatterns = [

    # For the main page
    path("", views.index, name="index"),

    # For fetching hotels of a certain city
    path('api/hotels/<str:city_name>/', views.get_hotels, name='get_hotels'),

    # For creating/updating hotels
    path('api/hotels/', views.manage_hotels, name="manage_hotels"),

    # For deleting hotels
    path('api/hotels/delete/<int:hotel_id>/', views.delete_hotel, name="delete_hotel")
]