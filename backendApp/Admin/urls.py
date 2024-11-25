from django.urls import path
from . import views

urlpatterns = [
    path('get_all_admins/<str:username>', views.get_all_admins, name='get_all_admins'),
    path('get_all_students', views.get_all_students, name='get_all_students'),
    path('get_all_faculty', views.get_all_faculty, name='get_all_faculty'),
    path('get_all_buildings', views.get_all_buildings, name='get_all_buildings'),
    path('get_all_rooms', views.get_all_rooms, name='get_all_rooms'),
    path('login', views.login, name='login'),
    path('add_faculity', views.add_faculty, name='add_faculty'),
    path('add_building', views.add_building, name='add_building'),
    path('add_room', views.add_room, name='add_room'),
    path('add_student', views.add_student, name='add_student'),
    path('add_admin', views.add_admin, name='add_admin'),
    path('remove_room', views.remove_room, name='remove_room'),
    path('remove_building/<int:building_id>', views.remove_building, name='remove_building'),
    path('delete_faculty/<int:faculty_id>', views.delete_faculty, name='delete_faculty'),
    path('add_item', views.add_item, name='add_item'),
    path('delete_item/<int:item_id>', views.delete_item, name='delete_item'),
    path('return_room', views.return_room, name='return_room'),
    path('return_item', views.return_item, name='return_item'),
    path('get_buildings_by_faculty/<str:faculty_name>/', views.get_buildings_by_faculty,
         name='get_buildings_by_faculty'),
    path('get_rooms_by_building/<str:building_name>/', views.get_rooms_by_building, name='get_rooms_by_building'),
    path('delete_student/<int:student_id>', views.delete_student, name='delete_student'),
    path('delete_admin/<int:admin_id>', views.delete_admin, name='delete_admin'),
    path('get_all_items', views.get_all_items, name='get_all_items'),
    path('get_reserved_rooms', views.get_reserved_rooms, name='get_reserved_rooms'),
    path('get_reserved_items', views.get_reserved_items, name='get_reserved_items'),
    path('types/', views.getTypes, name='get_types'),  # GET all types and POST create new type
    path('types/create/', views.createType, name='type-create'),  # POST create new type
    path('types/delete/', views.deleteType, name='type-delete'),  # DELETE type by ID
    path('types/<int:id>/', views.getType, name='attribute-detail'),

    # Attribute URLs
    path('attributes/', views.getAttributes, name='attribute-list'),
    # GET all attributes and POST create new attribute
    path('attributes/create/', views.createAttribute, name='attribute-create'),  # POST create new attribute
    path('attributes/<int:id>/', views.getAttribute , name='attribute-detail'),
    # GET, PUT, DELETE for specific attribute by ID
    path('attributes/delete/', views.deleteAttribute, name='attribute-delete'),  # DELETE attribute by ID
]
