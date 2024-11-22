from django.urls import path
from . import views

urlpatterns = [
    path('get_all_admins', views.get_all_admins, name='get_all_admins'),
    path('get_all_students', views.get_all_students, name='get_all_students'),
    path('get_all_faculity', views.get_all_faculty, name='get_all_faculty'),
    path('get_all_buildings', views.get_all_buildings, name='get_all_buildings'),
    path('get_all_rooms', views.get_all_rooms, name='get_all_rooms'),
    path('login', views.login, name='login'),
    path('add_faculity', views.add_faculty, name='add_faculty'),
    path('add_building', views.add_building, name='add_building'),
    path('add_room', views.add_room, name='add_room'),
    path('add_student', views.add_student, name='add_student'),
    path('add_admin', views.add_admin, name='add_admin'),
    path('remove_room/<int:room_id>', views.remove_room, name='remove_room'),
    path('remove_building/<int:building_id>', views.remove_building, name='remove_building'),
    path('delete_faculity/<int:faculity_id>', views.delete_faculty, name='delete_faculty'),
]
