from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
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


@ensure_csrf_cookie
@extend_schema(
    summary="Get all admins except the provided username",
    description="Fetch all admin users from the database except the one with the given username.",
    parameters=[
        {"name": "username", "in": "path", "required": True, "description": "Admin username to exclude", "schema": {"type": "string"}}
    ],
    responses={
        200: {"type": "object", "properties": {"admins": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "integer"}, "login": {"type": "string"}, "super_admin": {"type": "boolean"}}}}}},
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


@ensure_csrf_cookie
@extend_schema(
    summary="Get all students",
    description="Fetch all students from the database.",
    responses={
        200: {"type": "object", "properties": {"students": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "integer"}, "login": {"type": "string"}}}}}},
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
        200: {"type": "object", "properties": {"faculties": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "integer"}, "name": {"type": "string"}}}}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def get_all_faculty(request):
    """
    Fetch all faculties.
    """
    if request.method == "GET":
        faculties = Faculty.objects.all()
        faculty_list = [{"id": faculty.id, "name": faculty.name} for faculty in faculties]
        return JsonResponse({"faculties": faculty_list}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Get all buildings",
    description="Fetch all buildings from the database along with their faculty details.",
    responses={
        200: {"type": "object", "properties": {"buildings": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "integer"}, "name": {"type": "string"}, "faculty name": {"type": "string"}}}}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def get_all_buildings(request):
    """
    Fetch all buildings.
    """
    if request.method == "GET":
        buildings = Building.objects.all()
        building_list = [{"id": building.id, "name": building.name, "faculty name": building.faculty.name} for building
                         in buildings]
        return JsonResponse({"buildings": building_list}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Get all rooms",
    description="Fetch all rooms from the database, including rooms for rent and rooms with items.",
    responses={
        200: {"type": "object", "properties": {"rooms": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "integer"}, "number": {"type": "integer"}, "building_name": {"type": "string"}}}}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def get_all_rooms(request):
    """
    Fetch all rooms.
    """
    if request.method == "GET":
        rooms = RoomWithItems.objects.all()
        rooms2 = RoomToRent.objects.all()
        room_list = [{"id": room.id, "number": room.room_number, "building_name": room.building.name} for room in
                     rooms] + [
                        {"id": room.id, "number": room.room_number, "building_name": room.building.name} for room in
                        rooms2]
        return JsonResponse({"rooms": room_list}, status=200)
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
            admin_name = data.get('login')
            password = data.get('password')
            super_admin = bool(data.get('super_admin'))

            if not admin_name or not password:
                return JsonResponse({"error": "Invalid data. 'admin_name' and 'password' are required."}, status=400)

            new_admin = Admin.objects.create(username=admin_name, password=password, is_superuser=super_admin)
            return JsonResponse({"message": f"Admin '{new_admin.username}' added successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
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

            if not student_name or not password:
                return JsonResponse({"error": "Invalid data. 'student_name' and 'password' are required."}, status=400)

            new_student = Student.objects.create(username=student_name, password=password)
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
            admin_username = data.get('admin_username')

            if not faculty_name:
                return JsonResponse({"error": "Invalid data. 'faculty_name' is required."}, status=400)
            if not admin_username:
                return JsonResponse({"error": "Invalid data. 'admin_id' is required."}, status=400)

            try:
                admin = Admin.objects.get(username=admin_username)
            except Admin.DoesNotExist:
                return JsonResponse({"error": "Admin not found"}, status=404)

            new_faculty = Faculty.objects.create(name=faculty_name, admin=admin)
            return JsonResponse({"message": f"Faculty '{new_faculty.name}' added successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
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
            faculty_name = data.get('faculty_name')

            if not building_name:
                return JsonResponse({"error": "Invalid data. 'building_name' is required."}, status=400)

            if not faculty_name:
                return JsonResponse({"error": "Invalid data. 'faculty_name' is required."}, status=400)

            try:
                faculty = Faculty.objects.get(name=faculty_name)
            except Faculty.DoesNotExist:
                return JsonResponse({"error": "Faculty not found"}, status=404)

            new_building = Building.objects.create(name=building_name, faculty=faculty)
            return JsonResponse({"message": f"Building '{new_building.name}' added successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
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
            is_room_for_rent = bool(data.get('is_room_for_rent'))
            building_name = data.get('building_name')

            if not room_number:
                return JsonResponse({"error": "Invalid data. 'room_number' is required."}, status=400)

            if not building_name:
                return JsonResponse({"error": "Invalid data. 'building_name' is required."}, status=400)

            try:
                building = Building.objects.get(name=building_name)
            except Building.DoesNotExist:
                return JsonResponse({"error": "Building not found"}, status=404)

            if is_room_for_rent:
                new_room = RoomToRent.objects.create(room_number=room_number, building=building)
            else:
                new_room = RoomWithItems.objects.create(room_number=room_number, building=building)

            return JsonResponse({"message": f"Room '{new_room.room_number}' added successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
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
        {"name": "building_id", "in": "path", "required": True, "description": "ID of the building to delete", "schema": {"type": "integer"}}
    ],
    responses={
        200: {"type": "object", "properties": {"message": {"type": "string"}}},
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def remove_building(request, building_id):
    """
    Remove a building by ID.
    """
    if request.method == "DELETE":
        try:
            Building.objects.filter(id=building_id).delete()
            return JsonResponse({"message": f"Building {building_id} removed successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Delete a faculty by ID",
    description="Remove a faculty from the database using its unique ID.",
    parameters=[
        {"name": "faculty_id", "in": "path", "required": True, "description": "ID of the faculty to delete", "schema": {"type": "integer"}}
    ],
    responses={
        200: {"type": "object", "properties": {"message": {"type": "string"}}},
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def delete_faculty(request, faculty_id):
    """
    Delete a faculty by ID.
    """
    if request.method == "DELETE":
        try:
            faculty_deleted, _ = Faculty.objects.filter(id=faculty_id).delete()
            if faculty_deleted:
                return JsonResponse({"message": f"Faculty {faculty_id} deleted successfully"}, status=200)
            else:
                return JsonResponse({"error": "Faculty not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
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
            data = request.data
            name = data.get('name')
            amount = data.get('amount')
            room_id = data.get('room_with_items')
            item_type = data.get('type')  # Expecting a string
            attribute = data.get('attribute')  # Expecting a string

            if not all([name, amount, room_id, item_type, attribute]):
                return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the room
            RoomWithItems = apps.get_model('RoomWithItems', 'RoomWithItems')
            room = RoomWithItems.objects.get(id=room_id)

            # Create the item
            Item = apps.get_model('Item', 'Item')
            item = Item.objects.create(
                name=name,
                amount=amount,
                room_with_items=room,
                type=item_type,
                attribute=attribute
            )

            try:
                # Fetch type and attribute names
                type_name = data.get('type')
                attribute_name = data.get('attribute')

                # Validate if the type and attribute exist
                Type = apps.get_model('backendApp', 'Type')
                Attribute = apps.get_model('backendApp', 'Attribute')

                if not Type.objects.filter(type_name=type_name).exists():
                    return Response({'error': 'Invalid type name.'}, status=status.HTTP_400_BAD_REQUEST)
                if not Attribute.objects.filter(attribute_name=attribute_name).exists():
                    return Response({'error': 'Invalid attribute name.'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                    return Response({'Could not create type or attribute. Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': 'Item created successfully', 'item_id': item.id}, status=status.HTTP_201_CREATED)
        except RoomWithItems.DoesNotExist:
            return Response({'error': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@extend_schema(
    summary="Delete an item by ID",
    description="Remove an item from the database using its unique ID.",
    parameters=[
        {"name": "item_id", "in": "path", "required": True, "description": "ID of the item to delete", "schema": {"type": "integer"}}
    ],
    responses={
        200: {"type": "object", "properties": {"message": {"type": "string"}}},
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
        405: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
)
def delete_item(request, item_id):
    """
    Delete an item by ID.
    """
    if request.method == "DELETE":
        try:
            item_deleted, _ = Item.objects.filter(id=item_id).delete()
            if item_deleted:
                return JsonResponse({"message": f"Item {item_id} deleted successfully"}, status=200)
            else:
                return JsonResponse({"error": "Item not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
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
            room_id = data.get('room_id')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Validate that the room exists
        try:
            room = RoomToRent.objects.get(id=room_id)
        except RoomToRent.DoesNotExist:
            return JsonResponse({"error": "Room not found"}, status=404)

        # Check if the student has rented the room
        try:
            booking = Booking.objects.get(room_to_rent_id=room_id, user__username=reserved_by)
        except Booking.DoesNotExist:
            return JsonResponse({"error": "Booking not found"}, status=404)

        booking.end_time = datetime.now()
        booking.save()

        return JsonResponse({"message": f"Room {room_id} marked as returned by student {reserved_by} successfully"}, status=200)
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
def return_item(request):
    """
    Return an item by student ID and item ID.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            reserved_by = data.get('reserved_by')
            item_id = data.get('item_id')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Validate that the item exists
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)

        # Check if the student has rented the item
        try:
            booking = ItemBooking.objects.get(item_id=item_id, user__username=reserved_by)
        except ItemBooking.DoesNotExist:
            return JsonResponse({"error": "Booking not found"}, status=404)

        # Increase the item amount
        item.amount += 1
        item.save()

        # Delete the booking
        booking.delete()

        return JsonResponse({"message": f"Item {item_id} returned by student {reserved_by} successfully"}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Get buildings by faculty",
    description="Fetch all buildings associated with a given faculty name.",
    parameters=[
        {"name": "faculty_name", "in": "path", "required": True, "description": "Name of the faculty", "schema": {"type": "string"}}
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
    Get buildings by faculty name.
    """
    if request.method == "GET":
        try:
            faculty = Faculty.objects.get(name=faculty_name)
        except Faculty.DoesNotExist:
            return JsonResponse({"error": "Faculty not found"}, status=404)

        buildings = Building.objects.filter(faculty=faculty)
        buildings_data = [{"id": building.id, "name": building.name} for building in buildings]

        return JsonResponse({"buildings": buildings_data}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@extend_schema(
    summary="Get rooms by building",
    description="Fetch all rooms (both rentable and with items) associated with a given building name.",
    parameters=[
        {"name": "building_name", "in": "path", "required": True, "description": "Name of the building", "schema": {"type": "string"}}
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
        {"name": "student_id", "in": "path", "required": True, "description": "ID of the student to delete", "schema": {"type": "integer"}}
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
        {"name": "admin_id", "in": "path", "required": True, "description": "ID of the admin to delete", "schema": {"type": "integer"}}
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
    try:
        Item = apps.get_model('Item', 'Item')
        items = Item.objects.all()

        item_list = [{
            'id': item.id,
            'name': item.name,
            'amount': item.amount,
            'room_with_items': item.room_with_items.id,
            'type': item.type,
            'attribute': item.attribute
        } for item in items]

        return Response({'items': item_list}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    Fetch all reserved rooms.
    """
    if request.method == "GET":
        rooms = Booking.objects.select_related('room_to_rent', 'user')
        room_list = [
            {
                "id": room.room_to_rent.id,
                "room_number": room.room_to_rent.room_number,
                "building": room.room_to_rent.building.name,
                "faculty": room.room_to_rent.building.faculty.name,
                "start_date": room.start_time,
                "end_date": room.end_time,
                "reserved_by": room.user.username
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
            Item = apps.get_model('Item', 'Item')
            reserved_items = Item.objects.filter(amount__lt=10)  # Example filter

            item_list = [{
                'id': item.id,
                'name': item.name,
                'amount': item.amount,
                'room_with_items': item.room_with_items.id,
                'type': item.type,
                'attribute': item.attribute
            } for item in reserved_items]

            return Response({'reserved_items': item_list}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        bookings = Booking.objects.select_related('room_to_rent', 'user')
        booking_list = [
            {
                "id": booking.id,
                "room_id": booking.room_to_rent.id,
                "room_number": booking.room_to_rent.room_number,
                "building": booking.room_to_rent.building.name,
                "faculty": booking.room_to_rent.building.faculty.name,
                "reserved_by": booking.user.username,
                "start_time": booking.start_time,
                "end_time": booking.end_time
            }
            for booking in bookings
        ]
        return JsonResponse({"bookings": booking_list}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def getTypes(self, request):
    try:
        Type = apps.get_model('backendApp', 'Type')  # Update to match your app name
        types = Type.objects.all()

        type_list = [{'id': type.id, 'type_name': type.type_name} for type in types]
        return Response({'types': type_list}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@require_http_methods(["DELETE"])
def createType(self, request, *args, **kwargs):
    try:
        data = request.data
        type_name = data.get('type_name')

        if not type_name:
            return Response({'error': 'Type name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        Type = apps.get_model('backendApp', 'Type')  # Update to match your app name
        new_type = Type.objects.create(type_name=type_name)
        return Response({'message': 'Type created successfully', 'type_id': new_type.id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@require_http_methods(["DELETE"])
def deleteType(self, request, *args, **kwargs):
    try:
        Type = apps.get_model('backendApp', 'Type')  # Update to match your app name
        type_obj = Type.objects.get(id=type_id)
        type_obj.delete()
        return Response({'message': 'Type deleted successfully'}, status=status.HTTP_200_OK)
    except Type.DoesNotExist:
        return Response({'error': 'Type not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
def getAttributes(self, request, *args, **kwargs):
    # Fetch all Attributes
    try:
        Attribute = apps.get_model('backendApp', 'Attribute')  # Update to match your app name
        attributes = Attribute.objects.all()

        attribute_list = [{'id': attr.id, 'attribute_name': attr.attribute_name} for attr in attributes]
        return Response({'attributes': attribute_list}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@require_http_methods(["POST"])
def createAttribute(self, request, *args, **kwargs):
    try:
        data = request.data
        attribute_name = data.get('attribute_name')

        if not attribute_name:
            return Response({'error': 'Attribute name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        Attribute = apps.get_model('backendApp', 'Attribute')  # Update to match your app name
        new_attribute = Attribute.objects.create(attribute_name=attribute_name)
        return Response({'message': 'Attribute created successfully', 'attribute_id': new_attribute.id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@require_http_methods(["DELETE"])
def deleteAttribute(self, request, *args, **kwargs):
    try:
        Attribute = apps.get_model('backendApp', 'Attribute')  # Update to match your app name
        attribute = Attribute.objects.get(id=attribute_id)
        attribute.delete()
        return Response({'message': 'Attribute deleted successfully'}, status=status.HTTP_200_OK)
    except Attribute.DoesNotExist:
        return Response({'error': 'Attribute not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def getType(self, request, *args, **kwargs):
    if 'id' in kwargs:
    # Fetch a specific type by ID
        try:
            type_obj = Type.objects.get(id=kwargs['id'])
            return JsonResponse({'id': type_obj.id, 'type_name': type_obj.type_name})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Type not found"}, status=404)
    else:
        # Fetch all types
        types = Type.objects.all().values('id', 'type_name')
        return JsonResponse(list(types), safe=False)

def getAttribute(self, request, *args, **kwargs):
    if 'id' in kwargs:
    # Fetch a specific attribute by ID
        try:
            attribute_obj = Attribute.objects.get(id=kwargs['id'])
            return JsonResponse({'id': attribute_obj.id, 'attribute_name': attribute_obj.attribute_name})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Attribute not found"}, status=404)
    else:
        # Fetch all attributes
        attributes = Attribute.objects.all().values('id', 'attribute_name')
        return JsonResponse(list(attributes), safe=False)
