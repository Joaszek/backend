from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

from backendApp.Admin.models import Admin


@ensure_csrf_cookie
def get_all_admins(request):
    """
    Fetch all admin users.
    """
    if request.method == "GET":
        # Implement the logic here
        return JsonResponse({"message": "Endpoint 'get_all_admins' hit successfully"})
    return JsonResponse({"error": "Method not allowed"}, status=405)

@ensure_csrf_cookie
def get_all_students(request):
    """
    Fetch all students.
    """
    if request.method == "GET":
        # Implement the logic here
        return JsonResponse({"message": "Endpoint 'get_all_students' hit successfully"})
    return JsonResponse({"error": "Method not allowed"}, status=405)

@ensure_csrf_cookie
def get_all_faculty(request):
    """
    Fetch all faculties.
    """
    if request.method == "GET":
        # Implement the logic here
        return JsonResponse({"message": "Endpoint 'get_all_faculity' hit successfully"})
    return JsonResponse({"error": "Method not allowed"}, status=405)

@ensure_csrf_cookie
def get_all_buildings(request):
    """
    Fetch all buildings.
    """
    if request.method == "GET":
        # Implement the logic here
        return JsonResponse({"message": "Endpoint 'get_all_buildings' hit successfully"})
    return JsonResponse({"error": "Method not allowed"}, status=405)

@ensure_csrf_cookie
def get_all_rooms(request):
    """
    Fetch all rooms.
    """
    if request.method == "GET":
        # Implement the logic here
        return JsonResponse({"message": "Endpoint 'get_all_rooms' hit successfully"})
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

@ensure_csrf_cookie
def give_back_item_item_id(request):
    """
    Allow admin to mark an item as returned.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Implement the logic to mark the item as returned
        return JsonResponse({"message": f"Item {item_id} marked as returned successfully"})
    return JsonResponse({"error": "Method not allowed"}, status=405)

@ensure_csrf_cookie
def room_cancel_room_rental_room_id(request):
    """
    Cancel room rental by admin.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            room_id = data.get('room_id')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Implement the logic to cancel the room rental
        return JsonResponse({"message": f"Room rental for {room_id} cancelled successfully"})
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
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Implement the logic to add a faculty
        return JsonResponse({"message": f"Faculty '{faculty_name}' added successfully"})
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
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Implement the logic to add a building
        return JsonResponse({"message": f"Building '{building_name}' added successfully"})
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
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Implement the logic to add a room
        return JsonResponse({"message": f"Room '{room_number}' added successfully"})
    return JsonResponse({"error": "Method not allowed"}, status=405)

@ensure_csrf_cookie
def add_student(request):
    """
    Add a new student by admin.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            student_name = data.get('student_name')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Implement the logic to add a student
        return JsonResponse({"message": f"Student '{student_name}' added successfully"})
    return JsonResponse({"error": "Method not allowed"}, status=405)

@ensure_csrf_cookie
def add_admin(request):
    """
    Add a new admin user.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            admin_name = data.get('admin_name')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Implement the logic to add an admin
        return JsonResponse({"message": f"Admin '{admin_name}' added successfully"})
    return JsonResponse({"error": "Method not allowed"}, status=405)

@ensure_csrf_cookie
def remove_room_room_id(request):
    """
    Remove a room by ID.
    """
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            room_id = data.get('room_id')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Implement the logic to remove a room
        return JsonResponse({"message": f"Room {room_id} removed successfully"})
    return JsonResponse({"error": "Method not allowed"}, status=405)

@ensure_csrf_cookie
def edit_student_student_id(request):
    """
    Edit student details by ID.
    """
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Implement the logic to edit a student
        return JsonResponse({"message": f"Student {student_id} updated successfully"})
    return JsonResponse({"error": "Method not allowed"}, status=405)

@ensure_csrf_cookie
def remove_building_building_id(request):
    """
    Remove a building by ID.
    """
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            building_id = data.get('building_id')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Implement the logic to remove a building by ID
        return JsonResponse({"message": f"Building {building_id} removed successfully"})
    return JsonResponse({"error": "Method not allowed"}, status=405)

@ensure_csrf_cookie
def delete_faculty_faculty_id(request):
    """
    Delete a faculty by ID.
    """
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            faculty_id = data.get('faculty_id')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Implement the logic to delete a faculty by ID
        return JsonResponse({"message": f"Faculty {faculty_id} deleted successfully"})
    return JsonResponse({"error": "Method not allowed"}, status=405)

@ensure_csrf_cookie
def edit_admin_id(request):
    """
    Edit admin details by ID.
    """
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            admin_id = data.get('id')
            updated_data = data.get('updated_data')  # Adjust based on actual structure
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Implement the logic to edit an admin's details
        return JsonResponse({"message": f"Admin {admin_id} updated successfully"})
    return JsonResponse({"error": "Method not allowed"}, status=405)