from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

from backendApp.Admin.models import Admin
from backendApp.Booking.models import Booking
from backendApp.Building.models import Building
from backendApp.Faculty.models import Faculty
from backendApp.Item.models import Item
from backendApp.ItemBooking.models import ItemBooking
from backendApp.Student.models import Student
from backendApp.RoomWithItems.models import RoomWithItems
from backendApp.RoomToRent.models import RoomToRent


@ensure_csrf_cookie
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
def add_item(request):
    """
    Add a new item to a room.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            building_number = data.get('building_number')
            room_number = data.get('room_number')
            item_owner = data.get('item_owner')
            item_name = data.get('item_name')
            item_amount = data.get('item_amount')

            if not building_number:
                return JsonResponse({"error": "Invalid data. 'building_number' is required."}, status=400)
            if not room_number:
                return JsonResponse({"error": "Invalid data. 'room_number' is required."}, status=400)
            if not item_owner:
                return JsonResponse({"error": "Invalid data. 'item_owner' is required."}, status=400)
            if not item_name:
                return JsonResponse({"error": "Invalid data. 'item_name' is required."}, status=400)
            if item_amount is None:
                return JsonResponse({"error": "Invalid data. 'item_amount' is required."}, status=400)

            try:
                room = RoomWithItems.objects.get(building__name=building_number, room_number=room_number)
            except RoomWithItems.DoesNotExist:
                return JsonResponse({"error": "Room not found"}, status=404)

            new_item = Item.objects.create(
                name=item_name,
                amount=item_amount,
                room_with_items=room,
                item_owner=item_owner
            )
            return JsonResponse({"message": f"Item '{new_item.name}' added successfully"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
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
def return_room(request):
    """
    Return a room by room ID and student ID.
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

        # Delete the booking
        booking.delete()

        return JsonResponse({"message": f"Room {room_id} returned by student {reserved_by} successfully"}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
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
def get_all_items(request):
    """
    Fetch all items.
    """
    if request.method == "GET":
        items = Item.objects.all()
        item_list = [
            {
                "id": item.id,
                "name": item.name,
                "amount": item.amount,
                "room_id": item.room_with_items.id,
                "item_owner": item.item_owner,
                "room_number": item.room_with_items.room_number,
                "building": item.room_with_items.building.name,
                "faculty": item.room_with_items.building.faculty.name
            }
            for item in items
        ]
        return JsonResponse({"items": item_list}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
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
def get_reserved_items(request):
    """
    Fetch all reserved items.
    """
    if request.method == "GET":
        items = ItemBooking.objects.select_related('item', 'user')
        item_list = [
            {
                "id": item.item.id,
                "name": item.item.name,
                "item_owner": item.item.item_owner,
                "room_number": item.item.room_with_items.room_number,
                "building": item.item.room_with_items.building.name,
                "faculty": item.item.room_with_items.building.faculty.name,
                "start_date": item.start_date,
                "end_date": item.end_date,
                "reserved_by": item.user.username
            }
            for item in items
        ]
        return JsonResponse({"items": item_list}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)