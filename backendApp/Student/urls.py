from django.urls import path
from . import views

urlpatterns = [
    path('get_available_rooms', views.get_available_rooms, name='get_available_rooms'),
    path('get_available_items', views.get_available_items, name='get_available_items'),
    path('rent_item', views.rent_item, name='rent_item'),
    path('rent_room', views.rent_room, name='rent_room'),
]
