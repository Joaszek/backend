from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.apps import apps
from datetime import datetime

from django.views.decorators.http import require_http_methods
from drf_spectacular.utils import extend_schema

from backendApp import Attribute
from backendApp.Admin.models import Admin
from backendApp.Booking.models import Booking
from backendApp.Building.models import Building
from backendApp.Faculty.models import Faculty
from backendApp.Item.models import Item
from backendApp.ItemBooking.models import ItemBooking
from backendApp.Student.models import Student
from backendApp.RoomWithItems.models import RoomWithItems
from backendApp.RoomToRent.models import RoomToRent
from backendApp.Type.models import Type


@csrf_exempt
@extend_schema(
    summary="Get all admins except the provided username",
    description="Fetch all admin users from the database except the one with the given username.",
    parameters=[
        {"name": "username", "in": "path", "required": True, "description": "Admin username to exclude",
         "schema": {"type": "string"}}
    ],
    responses={
        200: {"type": "object", "properties": {"admins": {"type": "array", "items": {"type": "object", "properties": {
            "id": {"type": "integer"}, "login": {"type": "string"}, "super_admin": {"type": "boolean"}}}}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def get_all_admins(request, username):
    """
    Fetch all admin users except the one with the provided username.
    """
    if request.method == "GET":
        admins = Admin.objects.exclude(username=username)
        admin_list = [{"id": admin.id, "login": admin.username, "super_admin": admin.is_superuser} for admin in admins]
        return JsonResponse({"admins": admin_list}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Get all students",
    description="Fetch all students from the database.",
    responses={
        200: {"type": "object", "properties": {"students": {"type": "array", "items": {"type": "object", "properties": {
            "id": {"type": "integer"}, "login": {"type": "string"}}}}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def get_all_students(request):
    """
    Fetch all students.
    """
    if request.method == "GET":
        students = Student.objects.all()
        student_list = [{"id": student.id, "login": student.__str__()} for student in students]
        return JsonResponse({"students": student_list}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Get all faculties",
    description="Fetch all faculties from the database.",
    responses={
        200: {"type": "object", "properties": {"faculties": {"type": "array", "items": {"type": "object",
                                                                                        "properties": {
                                                                                            "id": {"type": "integer"},
                                                                                            "name": {
                                                                                                "type": "string"}}}}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def get_all_faculty(request):
    """
    Fetch all faculties.
    """
    if request.method == "GET":
        faculties = Faculty.objects.all()
        faculty_list = [{"id": faculty.faculty_id, "name": faculty.name, "admin": faculty.admin_id} for faculty in
                        faculties]
        return JsonResponse({"faculties": faculty_list}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Add a new admin",
    description="Create a new admin user. Requires `login`, `password`, and `super_admin` fields.",
    request={
        "type": "object",
        "properties": {
            "login": {"type": "string", "example": "admin123"},
            "password": {"type": "string", "example": "securepassword"},
            "super_admin": {"type": "boolean", "example": True}
        },
    },
    responses={
        200: {"type": "object", "properties": {"message": {"type": "string"}}},
        400: {"type": "object", "properties": {"error": {"type": "string"}}},
    },
)
def add_admin(request):
    """
    Add a new admin user.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            is_superuser = bool(data.get('is_superuser', False))  # Defaults to False if not provided
            additional_field = data.get('additional_field', '')
            first_name = data.get('first_name', 'Adam')  # Default value
            last_name = data.get('last_name', 'Kowalski')  # Default value
            is_staff = bool(data.get('is_staff', True))  # Defaults to True
            is_active = bool(data.get('is_active', True))  # Defaults to True

            # Validate required fields
            if not username or not password:
                return JsonResponse(
                    {"error": "Invalid data. 'username', 'password', and 'email' are required."},
                    status=400
                )

            # Create a new admin user with hashed password
            new_admin = Admin.objects.create(
                username=username,
                password=password,  # Hash the password
                is_superuser=is_superuser,
                additional_field=additional_field,
                first_name=first_name,
                last_name=last_name,
                is_staff=is_staff,
                is_active=is_active,
            )

            return JsonResponse({"message": f"Admin '{new_admin.username}' added successfully"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Add a new student",
    description="Add a new student to the system by providing a username and password.",
    request={
        "type": "object",
        "properties": {
            "username": {"type": "string", "example": "student123"},
            "password": {"type": "string", "example": "securepassword"}
        },
    },
    responses={
        200: {"type": "object", "properties": {"message": {"type": "string"}}},
        400: {"type": "object", "properties": {"error": {"type": "string"}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def add_student(request):
    """
    Add a new student by admin.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            student_name = data.get('username')
            password = data.get('password')
            additional_field = data.get("additional_field")

            if not student_name or not password:
                return JsonResponse({"error": "Invalid data. 'student_name' and 'password' are required."}, status=400)

            new_student = Student.objects.create(username=student_name, password=password,
                                                 additional_field=additional_field)
            return JsonResponse({"message": f"Student '{new_student.username}' added successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Add a new faculty",
    description="Add a new faculty by providing the faculty name and the username of an associated admin.",
    request={
        "type": "object",
        "properties": {
            "faculty_name": {"type": "string", "example": "Engineering"},
            "admin_username": {"type": "string", "example": "admin123"}
        },
    },
    responses={
        200: {"type": "object", "properties": {"message": {"type": "string"}}},
        400: {"type": "object", "properties": {"error": {"type": "string"}}},
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def add_faculty(request):
    """
    Add a new faculty by admin.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            faculty_name = data.get('faculty_name')
            admin_id = '123456' # Default value
            if not faculty_name:
                return JsonResponse({"error": "Invalid data. 'faculty_name' is required."}, status=400)
            if not admin_id:
                return JsonResponse({"error": "Invalid data. 'admin_id' is required."}, status=400)

            # Create and save new Faculty instance
            new_faculty = Faculty.objects.create(name=faculty_name, admin_id=admin_id)
            return JsonResponse({"message": f"Faculty '{new_faculty.name}' added successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Add a new building",
    description="Add a new building by providing its name and the associated faculty name.",
    request={
        "type": "object",
        "properties": {
            "building_name": {"type": "string", "example": "Building A"},
            "faculty_name": {"type": "string", "example": "Engineering"}
        },
    },
    responses={
        200: {"type": "object", "properties": {"message": {"type": "string"}}},
        400: {"type": "object", "properties": {"error": {"type": "string"}}},
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def add_building(request):
    """
    Add a new building by admin.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            building_name = data.get('building_name')
            faculty_name = data.get('faculty_name')  # Matches the 'faculty' field in the Building model

            # Validate input
            if not building_name:
                return JsonResponse({"error": "Invalid data. 'building_name' is required."}, status=400)
            if not faculty_name:
                return JsonResponse({"error": "Invalid data. 'faculty_name' is required."}, status=400)

            # Create and save new Building instance
            new_building = Building.objects.create(name=building_name, faculty=faculty_name)
            return JsonResponse({"message": f"Building '{new_building.name}' added successfully"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Add a new room",
    description="Add a new room by providing its number, whether it's for rent, and the building name.",
    request={
        "type": "object",
        "properties": {
            "room_number": {"type": "integer", "example": 101},
            "is_room_for_rent": {"type": "boolean", "example": True},
            "building_name": {"type": "string", "example": "Building A"}
        },
    },
    responses={
        200: {"type": "object", "properties": {"message": {"type": "string"}}},
        400: {"type": "object", "properties": {"error": {"type": "string"}}},
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def add_room(request):
    """
    Add a new room by admin.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            room_number = data.get('room_number')
            is_room_for_rent = data.get('is_room_for_rent', False)
            building_name = data.get('building_name')
            faculty_name = data.get('faculty_name')

            # Validate input
            if not room_number:
                return JsonResponse({"error": "Invalid data. 'room_number' is required."}, status=400)
            if not building_name:
                return JsonResponse({"error": "Invalid data. 'building_name' is required."}, status=400)

            # Create a new room
            if is_room_for_rent:
                new_room = RoomToRent.objects.create(
                    room_number=room_number,
                    building=building_name,  # Store building name as string
                    faculty=faculty_name
                )
            else:
                new_room = RoomWithItems.objects.create(
                    room_number=room_number,
                    building=building_name,  # Store building name as string
                    faculty=faculty_name
                )

            return JsonResponse({"message": f"Room '{new_room.room_number}' added successfully"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Remove a room",
    description="Remove a room by providing its ID and whether it's a room for rent.",
    request={
        "type": "object",
        "properties": {
            "room_id": {"type": "integer", "example": 1},
            "is_room_for_rent": {"type": "boolean", "example": True}
        },
    },
    responses={
        200: {"type": "object", "properties": {"message": {"type": "string"}}},
        400: {"type": "object", "properties": {"error": {"type": "string"}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def remove_room(request):
    """
    Remove a room by ID.
    """
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            room_id = data.get('room_id')
            is_room_for_rent = bool(data.get('is_room_for_rent'))

            if not room_id:
                return JsonResponse({"error": "Invalid data. 'room_id' is required."}, status=400)

            if is_room_for_rent:
                RoomToRent.objects.filter(id=room_id).delete()
            else:
                RoomWithItems.objects.filter(id=room_id).delete()

            return JsonResponse({"message": f"Room {room_id} removed successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Remove a building by ID",
    description="Delete a building from the database using its unique ID.",
    parameters=[
        {"name": "building_id", "in": "path", "required": True, "description": "ID of the building to delete",
         "schema": {"type": "integer"}}
    ],
    responses={
        200: {"type": "object", "properties": {"message": {"type": "string"}}},
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def remove_building(request, building_id):
    """
    Remove a building by ID and delete associated rooms in RoomToRent and RoomWithItems tables.
    """
    if request.method == "DELETE":
        try:
            # Check if the building exists
            building = Building.objects.filter(id=building_id).first()
            if not building:
                return JsonResponse({"error": f"Building with ID {building_id} not found"}, status=404)

            # Delete rooms in RoomToRent and RoomWithItems associated with the building
            RoomToRent.objects.filter(building=building.name).delete()
            RoomWithItems.objects.filter(building=building.name).delete()

            # Delete the building itself
            building.delete()

            return JsonResponse({"message": f"Building {building_id} and its associated rooms removed successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)



@csrf_exempt
@extend_schema(
    summary="Delete a faculty by ID",
    description="Remove a faculty from the database using its unique ID.",
    parameters=[
        {"name": "faculty_id", "in": "path", "required": True, "description": "ID of the faculty to delete",
         "schema": {"type": "integer"}}
    ],
    responses={
        200: {"type": "object", "properties": {"message": {"type": "string"}}},
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def delete_faculty(request, faculty_id):
    """
    Delete a faculty by ID, along with its associated buildings and rooms.
    """
    if request.method == "DELETE":
        try:
            faculty = Faculty.objects.filter(faculty_id=faculty_id).first()
            if not faculty:
                return JsonResponse({"error": f"Faculty with ID {faculty_id} not found"}, status=404)

            buildings = Building.objects.filter(faculty=faculty.name)

            for building in buildings:
                RoomToRent.objects.filter(building=building.name).delete()
                RoomWithItems.objects.filter(building=building.name).delete()

            buildings.delete()

            faculty.delete()

            return JsonResponse({"message": f"Faculty {faculty_id} and its associated buildings and rooms removed successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Add a new item to a room",
    description="Create a new item and assign it to a specific room by providing details like the room number, building name, item owner, and quantity.",
    request={
        "type": "object",
        "properties": {
            "building_number": {"type": "string", "example": "Building A"},
            "room_number": {"type": "integer", "example": 101},
            "item_owner": {"type": "string", "example": "Admin"},
            "item_name": {"type": "string", "example": "Laptop"},
            "item_amount": {"type": "integer", "example": 10}
        },
    },
    responses={
        201: {"type": "object", "properties": {"message": {"type": "string"}}},
        400: {"type": "object", "properties": {"error": {"type": "string"}}},
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def add_item(request):
    """
    Add a new item to a room.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get('name')
            amount = data.get('amount')
            room_id = data.get('room_with_items')
            item_type = data.get('type')
            attribute = data.get('attribute')
            faculty = data.get('faculty')
            building = data.get('building')

            # Create the item
            Item = apps.get_model('Item', 'Item')
            item = Item.objects.create(
                name=name,
                amount=amount,
                room_number=room_id,
                type=item_type,
                attribute=attribute,
                faculty=faculty,
                building=building
            )

            return JsonResponse({'message': 'Item created successfully', 'item_id': item.item_id}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed.'}, status=405)


@csrf_exempt
@extend_schema(
    summary="Delete an item by ID",
    description="Remove an item from the database using its unique ID.",
    parameters=[
        {"name": "item_id", "in": "path", "required": True, "description": "ID of the item to delete",
         "schema": {"type": "integer"}}
    ],
    responses={
        200: {"type": "object", "properties": {"message": {"type": "string"}}},
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def delete_item(request, item_id):
    """
    Delete an item by name.
    """
    if request.method == "DELETE":
        try:
            item_deleted, _ = Item.objects.filter(item_id=item_id).delete()
            if item_deleted:
                return JsonResponse({"message": f"Item '{item_id}' deleted successfully"}, status=200)
            else:
                return JsonResponse({"error": f"Item with name '{item_id}' not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Return a rented room",
    description="Mark a room as returned by updating the Booking record's `end_time`. Provide the `room_id` and the student username (`reserved_by`).",
    request={
        "type": "object",
        "properties": {
            "reserved_by": {"type": "string", "example": "student123"},
            "room_id": {"type": "integer", "example": 1}
        },
    },
    responses={
        200: {"type": "object", "properties": {"message": {"type": "string"}}},
        400: {"type": "object", "properties": {"error": {"type": "string"}}},
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def return_room(request):
    """
    Mark a room as returned by updating the Booking record.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            reserved_by = data.get('reserved_by')
            room_number = data.get('room_number')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Validate that the room exists
        try:
            room = RoomToRent.objects.get(room_number=room_number)
        except RoomToRent.DoesNotExist:
            return JsonResponse({"error": "Room not found"}, status=404)

        # Check if the student has rented the room
        try:
            booking = Booking.objects.get(room_number=room_number, user=reserved_by)
        except Booking.DoesNotExist:
            return JsonResponse({"error": "Booking not found"}, status=404)

        booking.end_time = datetime.now()
        booking.returned = True
        booking.save()

        room.available = True
        room.save()

        return JsonResponse({"message": f"Room {room_number} marked as returned by student {reserved_by} successfully"},
                            status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Return a rented item",
    description="Mark an item as returned by increasing the item's quantity and deleting the booking record. Provide the `item_id` and the student username (`reserved_by`).",
    request={
        "type": "object",
        "properties": {
            "reserved_by": {"type": "string", "example": "student123"},
            "item_id": {"type": "integer", "example": 1}
        },
    },
    responses={
        200: {"type": "object", "properties": {"message": {"type": "string"}}},
        400: {"type": "object", "properties": {"error": {"type": "string"}}},
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
@csrf_exempt
def return_item(request):
    """
    Return an item by student ID and item ID.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            reserved_by = data.get('reserved_by')
            item_id = data.get('id')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        try:
            item = Item.objects.get(item_id=item_id)
        except Item.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)

        itemBookings = ItemBooking.objects.filter(item_id=item_id, student_id=reserved_by, returned=False)
        if not itemBookings.exists():
            return JsonResponse({"error": "Booking not found or already returned"}, status=404)

        # Increase the item amount
        item.amount += 1
        item.save()

        # Update the bookings to mark them as returned
        for itemBooking in itemBookings:
            itemBooking.end_date = datetime.now().strftime('%Y-%m-%d')
            itemBooking.returned = True
            itemBooking.save()

        return JsonResponse({"message": f"Item {item_id} returned by student {reserved_by} successfully"}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Get buildings by faculty",
    description="Fetch all buildings associated with a given faculty name.",
    parameters=[
        {"name": "faculty_name", "in": "path", "required": True, "description": "Name of the faculty",
         "schema": {"type": "string"}}
    ],
    responses={
        200: {
            "type": "object",
            "properties": {
                "buildings": {
                    "type": "array",
                    "items": {"type": "object", "properties": {"id": {"type": "integer"}, "name": {"type": "string"}}}
                }
            }
        },
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def get_buildings_by_faculty(request, faculty_name):
    """
    Get buildings by faculty name along with RoomToRent and RoomWithItems data.
    """
    if request.method == "GET":
        try:
            # Filter buildings where the faculty name matches the given input
            buildings = Building.objects.filter(faculty__icontains=faculty_name)

            if not buildings.exists():
                return JsonResponse({"buildings": []}, status=200)

            # Collect data for each building
            buildings_data = []
            for building in buildings:
                # Fetch RoomToRent and RoomWithItems for the building
                room_to_rent = RoomToRent.objects.filter(building=building.name)
                room_with_items = RoomWithItems.objects.filter(building=building.name)

                # Serialize room data
                room_to_rent_data = [
                    {
                        "id": room.id,
                        "room_number": room.room_number,
                        "is_to_rent": room.is_to_rent,
                        "building": room.building,
                        "faculty": room.faculty,
                    }
                    for room in room_to_rent
                ]

                room_with_items_data = [
                    {
                        "id": room.id,
                        "room_number": room.room_number,
                        "is_to_rent": room.is_to_rent,
                        "building": room.building,
                        "faculty": room.faculty,
                    }
                    for room in room_with_items
                ]

                # Append building data with room details
                buildings_data.append({
                    "id": building.id,
                    "name": building.name,
                    "RoomToRent": room_to_rent_data,
                    "RoomWithItems": room_with_items_data,
                })

            return JsonResponse({"buildings": buildings_data}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Get rooms by building",
    description="Fetch all rooms (both rentable and with items) associated with a given building name.",
    parameters=[
        {"name": "building_name", "in": "path", "required": True, "description": "Name of the building",
         "schema": {"type": "string"}}
    ],
    responses={
        200: {
            "type": "object",
            "properties": {
                "rooms": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "number": {"type": "integer"},
                            "type": {"type": "boolean"}
                        }
                    }
                }
            }
        },
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def get_rooms_by_building(request, building_name):
    """
    Get all rooms by building name.
    """
    if request.method == "GET":
        try:
            building = Building.objects.get(name=building_name)
        except Building.DoesNotExist:
            return JsonResponse({"error": "Building not found"}, status=404)

        rooms = RoomWithItems.objects.filter(building=building)
        rooms2 = RoomToRent.objects.filter(building=building)
        rooms_data = ([{"id": room.id, "number": room.room_number, "type": room.is_to_rent} for room in rooms]
                      + [{"id": room.id, "number": room.room_number, "type": room.is_to_rent} for room in rooms2])

        rooms_data.sort(key=lambda x: x["number"])

        return JsonResponse({"rooms": rooms_data}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Delete a student by ID",
    description="Remove a student from the database using their unique ID.",
    parameters=[
        {"name": "student_id", "in": "path", "required": True, "description": "ID of the student to delete",
         "schema": {"type": "integer"}}
    ],
    responses={
        200: {"type": "object", "properties": {"message": {"type": "string"}}},
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def delete_student(request, student_id):
    """
    Delete a student by ID.
    """
    if request.method == "DELETE":
        try:
            student_deleted, _ = Student.objects.filter(id=student_id).delete()
            if student_deleted:
                return JsonResponse({"message": f"Student {student_id} deleted successfully"}, status=200)
            else:
                return JsonResponse({"error": "Student not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Delete an admin by ID",
    description="Remove an admin from the database using their unique ID.",
    parameters=[
        {"name": "admin_id", "in": "path", "required": True, "description": "ID of the admin to delete",
         "schema": {"type": "integer"}}
    ],
    responses={
        200: {"type": "object", "properties": {"message": {"type": "string"}}},
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def delete_admin(request, admin_id):
    """
    Delete an admin by ID.
    """
    if request.method == "DELETE":
        try:
            admin_deleted, _ = Admin.objects.filter(id=admin_id).delete()
            if admin_deleted:
                return JsonResponse({"message": f"Admin {admin_id} deleted successfully"}, status=200)
            else:
                return JsonResponse({"error": "Admin not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Fetch all items",
    description="Retrieve a list of all items, including their room, building, and faculty details.",
    responses={
        200: {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                            "amount": {"type": "integer"},
                            "room_id": {"type": "integer"},
                            "item_owner": {"type": "string"},
                            "room_number": {"type": "integer"},
                            "building": {"type": "string"},
                            "faculty": {"type": "string"}
                        }
                    }
                }
            }
        },
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def get_all_items(request):
    """
    Fetch all items.
    """

    print("Entered function")
    if request.method == "GET":
        try:
            Item = apps.get_model('Item', 'Item')
            items = Item.objects.all()
            print("Items in the database: ", items)
            item_list = [{
                'id': item.item_id,
                'name': item.name,
                'amount': item.amount,
                'type': item.type,
                'room_number': item.room_number,
                'attribute': item.attribute,
                'user': item.user,
                'building': item.building,
                'faculty': item.faculty
            } for item in items]

            return JsonResponse({'items': item_list}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@extend_schema(
    summary="Admin login",
    description="Authenticate an admin user by providing their username and password.",
    request={
        "type": "object",
        "properties": {
            "username": {"type": "string", "example": "admin123"},
            "password": {"type": "string", "example": "securepassword"}
        },
    },
    responses={
        200: {"type": "object", "properties": {"message": {"type": "string"}, "csrf_token": {"type": "string"}}},
        401: {"type": "object", "properties": {"error": {"type": "string"}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def login(request):
    """
    Handle admin login.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Query the Admin model
        try:
            admin = Admin.objects.get(username=username)
        except Admin.DoesNotExist:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

        # Compare passwords
        if admin.check_password(password):
            csrf_token = get_token(request)
            return JsonResponse({
                "message": "Login successful",
                "csrf_token": csrf_token
            }, status=200)

        return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Invalid method"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Fetch all reserved rooms",
    description="Retrieve all reserved rooms with details such as building, faculty, and reservation period.",
    responses={
        200: {
            "type": "object",
            "properties": {
                "rooms": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "room_number": {"type": "integer"},
                            "building": {"type": "string"},
                            "faculty": {"type": "string"},
                            "start_date": {"type": "string", "format": "date"},
                            "end_date": {"type": "string", "format": "date"},
                            "reserved_by": {"type": "string"}
                        }
                    }
                }
            }
        },
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def get_reserved_rooms(request):
    """
    Fetch all reserved rooms filtered by user and is_to_rent=True.
    """
    if request.method == "GET":
        # Get the username from the query parameters

        # Filter bookings based on the user and is_to_rent=True
        rooms = Booking.objects.filter(isRoomToRent=True, returned=False)
        if not rooms.exists():
            return JsonResponse({"rooms": []}, status=200)

        room_list = [
            {
                "id": room.booking_id,
                "room_number": room.room_number,
                "building": room.building,
                "faculty": room.faculty,
                "start_date": room.start_time,
                "end_date": room.end_time,
                "reserved_by": room.user
            }
            for room in rooms
        ]

        return JsonResponse({"rooms": room_list}, status=200)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Fetch all reserved items",
    description="Retrieve all reserved items with details such as room, building, faculty, and reservation period.",
    responses={
        200: {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                            "item_owner": {"type": "string"},
                            "room_number": {"type": "integer"},
                            "building": {"type": "string"},
                            "faculty": {"type": "string"},
                            "start_date": {"type": "string", "format": "date"},
                            "end_date": {"type": "string", "format": "date"},
                            "reserved_by": {"type": "string"}
                        }
                    }
                }
            }
        },
        405: {"type": "object", "properties": {"error": {"type": "string"}}}})
def get_reserved_items(request):
    """
    Fetch all reserved items.
    """
    if request.method == "GET":
        try:
            ItemBooking = apps.get_model('ItemBooking', 'ItemBooking')
            reserved_items = ItemBooking.objects.filter(returned=False)

            item_list = [{
                'id': item_booking.id,
                'item_id': item_booking.item_id,
                'student_id': item_booking.student_id,
                'start_date': item_booking.start_date,
                'end_date': item_booking.end_date
            } for item_booking in reserved_items]

            return JsonResponse({'reserved_items': item_list}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Get all bookings",
    description="Retrieve all bookings from the database with details such as room number, building, faculty, reserved by, and the booking period.",
    responses={
        200: {
            "type": "object",
            "properties": {
                "bookings": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "room_id": {"type": "integer"},
                            "room_number": {"type": "integer"},
                            "building": {"type": "string"},
                            "faculty": {"type": "string"},
                            "reserved_by": {"type": "string"},
                            "start_time": {"type": "string", "format": "date"},
                            "end_time": {"type": "string", "format": "date"}
                        }
                    }
                }
            }
        },
        405: {"type": "object", "properties": {"error": {"type": "string"}}},
    },
)
def get_all_bookings(request):
    """
    Fetch all bookings.
    """
    if request.method == "GET":
        bookings = Booking.objects.filter(returned=True)

        if len(bookings) == 0:
            return JsonResponse({"bookings": []}, status=200)

        booking_list = [
            {
                "id": booking.booking_id,
                "item_id": booking.item_id,
                "room_number": booking.room_number,
                "user": booking.user,
                "building": booking.building,
                "faculty": booking.faculty,
                "start_time": booking.start_time,
                "end_time": booking.end_time,
                "isRoomToRent": booking.isRoomToRent
            }
            for booking in bookings
        ]

        return JsonResponse({"bookings": booking_list}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def getTypes(request):
    try:
        Type = apps.get_model('Type', 'Type')  # Update to match your app name
        types = Type.objects.all()

        type_list = [{'id': type.id, 'type_name': type.type_name} for type in types]
        return JsonResponse({'types': type_list}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def createType(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            type_name = data.get('type_name')

            if not type_name:
                return JsonResponse({'error': 'Type name is required.'}, status=400)

            Type = apps.get_model('Type', 'Type')
            type = Type.objects.create(type_name=type_name)
            return JsonResponse({'message': 'Type created successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def deleteType(request):

    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            type_id = data.get('id')
            Type = apps.get_model('Type', 'Type')  # Update to match your app name
            type_obj = Type.objects.get(id=type_id)
            type_obj.delete()
            return JsonResponse({'message': 'Type deleted successfully'}, status=200)
        except Type.DoesNotExist:
            return JsonResponse({'error': 'Type not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def getAttributes(request):
    # Fetch all Attributes
    try:
        Attribute = apps.get_model('Attribute', 'Attribute')  # Update to match your app name
        attributes = Attribute.objects.all()

        attribute_list = [{'id': attr.id, 'attribute_name': attr.attribute_name} for attr in attributes]
        return JsonResponse({'attributes': attribute_list}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def createAttribute(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            attribute_name = data.get('attribute_name')

            if not attribute_name:
                return JsonResponse({'error': 'Attribute name is required.'}, status=400)

            Attribute = apps.get_model('Attribute', 'Attribute')  # Update to match your app name
            new_attribute = Attribute.objects.create(attribute_name=attribute_name)
            return JsonResponse({'message': 'Attribute created successfully', 'attribute_id': new_attribute.id}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def deleteAttribute(request):

    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            attribute_id = data.get('id')

            Attribute = apps.get_model('Attribute', 'Attribute')  # Update to match your app name
            attribute = Attribute.objects.get(id=attribute_id)
            attribute.delete()
            return JsonResponse({'message': 'Attribute deleted successfully'}, status=200)
        except Attribute.DoesNotExist:
            return JsonResponse({'error': 'Attribute not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_returned_item_bookings(request):
    """
    Fetch all item bookings where returned is True.
    """
    try:
        item_bookings = ItemBooking.objects.filter(returned=True)
        booking_list = [
            {
                "id": booking.id,
                "item_id": booking.item_id,
                "student_id": booking.student_id,
                "start_date": booking.start_date,
                "end_date": booking.end_date,
                "returned": booking.returned
            }
            for booking in item_bookings
        ]
        return JsonResponse({"item_bookings": booking_list}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)