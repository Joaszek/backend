from django.urls import path
from . import views

urlpatterns = [
    path('get_all_admins', views.get_all_admins, name='get_all_admins'),
    path('get_all_students', views.get_all_students, name='get_all_students'),
    path('get_all_faculity', views.get_all_faculty, name='get_all_faculty'),
    path('get_all_buildings', views.get_all_buildings, name='get_all_buildings'),
    path('get_all_rooms', views.get_all_rooms, name='get_all_rooms'),
    path('login', views.login, name='login'),
    path('give_back_item/<int:item_id>', views.give_back_item_item_id, name='give_back_item'),
    path('room/cancel_room_rental/<int:room_id>', views.room_cancel_room_rental_room_id, name='cancel_room_rental'),
    path('add_faculity', views.add_faculty, name='add_faculty'),
    path('add_building', views.add_building, name='add_building'),
    path('add_room', views.add_room, name='add_room'),
    path('add_student', views.add_student, name='add_student'),
    path('add_admin', views.add_admin, name='add_admin'),
    path('remove_room/<int:room_id>', views.remove_room_room_id, name='remove_room'),
    path('remove_building/<int:building_id>', views.remove_building_building_id, name='remove_building'),
    path('delete_faculity/<int:faculity_id>', views.delete_faculty_faculty_id, name='delete_faculty'),
    path('edit_student/<int:student_id>', views.edit_student_student_id, name='edit_student'),
    path('edit_admin/<int:id>', views.edit_admin_id, name='edit_admin'),
]
