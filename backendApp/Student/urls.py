from django.urls import path
from . import views

urlpatterns = [
    path('get_available_rooms/<str:username>', views.get_available_rooms, name='get_available_rooms'),
    path('get_available_items', views.get_available_items, name='get_available_items'),
    path('rent_item', views.rent_item, name='rent_item'),
    path('rent_room', views.rent_room, name='rent_room'),
    path('reserved_items/<str:username>', views.get_reserved_items, name='get_reserved_items'),
    path('reserved_rooms/<str:username>', views.get_reserved_rooms, name='get_reserved_rooms'),
]