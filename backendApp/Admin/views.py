from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

from backendApp.Admin.models import Admin
from backendApp.Building.models import Building
from backendApp.Faculty.models import Faculty
from backendApp.Student.models import Student
from backendApp.RoomWithItems.models import RoomWithItems
from backendApp.RoomToRent.models import RoomToRent


@ensure_csrf_cookie
def get_all_admins(request):
    """
    Fetch all admin users.
    """
    if request.method == "GET":
        admins = Admin.objects.all()
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


@ensure_csrf_cookie
def get_all_faculty(request):
    """
    Fetch all faculties.
    """
    if request.method == "GET":
        faculties = Faculty.objects.all()
        faculty_list = [{"id": faculty.id, "name": faculty.name} for faculty in faculties]
        return JsonResponse({"faculties": faculty_list}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@ensure_csrf_cookie
def get_all_buildings(request):
    """
    Fetch all buildings.
    """
    if request.method == "GET":
        buildings = Building.objects.all()
        building_list = [{"id": building.id, "name": building.name} for building in buildings]
        return JsonResponse({"buildings": building_list}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@ensure_csrf_cookie
def get_all_rooms(request):
    """
    Fetch all rooms.
    """
    if request.method == "GET":
        rooms = RoomWithItems.objects.all()
        rooms2 = RoomToRent.objects.all()
        room_list = [{"id": room.id, "number": room.room_number} for room in rooms] + [
            {"id": room.id, "number": room.room_number} for room in rooms2]
        return JsonResponse({"rooms": room_list}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@ensure_csrf_cookie
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
            return JsonResponse({"message": f"Admin '{new_admin.username}' added successfully"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@ensure_csrf_cookie
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
            return JsonResponse({"message": f"Student '{new_student.username}' added successfully"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@ensure_csrf_cookie
def add_faculty(request):
    """
    Add a new faculty by admin.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            faculty_name = data.get('faculty_name')
            admin_id = data.get('admin_id')

            if not faculty_name:
                return JsonResponse({"error": "Invalid data. 'faculty_name' is required."}, status=400)
            if not admin_id:
                return JsonResponse({"error": "Invalid data. 'admin_id' is required."}, status=400)

            try:
                admin = Admin.objects.get(id=admin_id)
            except Admin.DoesNotExist:
                return JsonResponse({"error": "Admin not found"}, status=404)

            new_faculty = Faculty.objects.create(name=faculty_name, admin=admin)
            return JsonResponse({"message": f"Faculty '{new_faculty.name}' added successfully"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@ensure_csrf_cookie
def add_building(request):
    """
    Add a new building by admin.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            building_name = data.get('building_name')

            if not building_name:
                return JsonResponse({"error": "Invalid data. 'building_name' is required."}, status=400)

            new_building = Building.objects.create(name=building_name)
            return JsonResponse({"message": f"Building '{new_building.name}' added successfully"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@ensure_csrf_cookie
def add_room(request):
    """
    Add a new room by admin.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            room_number = data.get('room_number')
            is_room_for_rent = bool(data.get('is_room_for_rent'))

            if not room_number:
                return JsonResponse({"error": "Invalid data. 'room_number' is required."}, status=400)

            if is_room_for_rent:
                new_room = RoomToRent.objects.create(room_number=room_number)
            else:
                new_room = RoomWithItems.objects.create(room_number=room_number)

            return JsonResponse({"message": f"Room '{new_room.room_number}' added successfully"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@ensure_csrf_cookie
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


@ensure_csrf_cookie
def remove_building(request):
    """
    Remove a building by ID.
    """
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            building_id = data.get('building_id')

            if not building_id:
                return JsonResponse({"error": "Invalid data. 'building_id' is required."}, status=400)

            Building.objects.filter(id=building_id).delete()
            return JsonResponse({"message": f"Building {building_id} removed successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@ensure_csrf_cookie
def delete_faculty(request):
    """
    Delete a faculty by ID.
    """
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            faculty_id = data.get('faculty_id')

            if not faculty_id:
                return JsonResponse({"error": "Invalid data. 'faculty_id' is required."}, status=400)

            faculty_deleted, _ = Faculty.objects.filter(id=faculty_id).delete()
            if faculty_deleted:
                return JsonResponse({"message": f"Faculty {faculty_id} deleted successfully"}, status=200)
            else:
                return JsonResponse({"error": "Faculty not found"}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
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
