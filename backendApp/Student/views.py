from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
import json
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

@csrf_exempt
def student_login(request):
    """
    Handle student login.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            csrf_token = get_token(request)
            return JsonResponse({
                "message": "Login successful",
                "csrf_token": csrf_token
            }, status=200)

        return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Invalid method"}, status=405)

@ensure_csrf_cookie
def get_available_rooms(request):
    """
    Fetch available rooms for students.
    """
    if request.method == "GET":
        # Fetch any necessary data from request.GET if needed
        return JsonResponse({"message": "Endpoint 'get_available_rooms' hit successfully"})
    return JsonResponse({"error": "Method not allowed"}, status=405)

@ensure_csrf_cookie
def get_available_items(request):
    """
    Fetch available items for students.
    """
    if request.method == "GET":
        # Fetch any necessary data from request.GET if needed
        return JsonResponse({"message": "Endpoint 'get_available_items' hit successfully"})
    return JsonResponse({"error": "Method not allowed"}, status=405)

@ensure_csrf_cookie
def rent_item(request):
    """
    Allow students to rent an item.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
            item_id = data.get('item_id')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Implement the logic for renting an item
        return JsonResponse({
            "message": f"Student {student_id} rented item {item_id} successfully"
        })
    return JsonResponse({"error": "Method not allowed"}, status=405)

@ensure_csrf_cookie
def rent_room(request):
    """
    Allow students to rent a room.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
            room_id = data.get('room_id')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Implement the logic for renting a room
        return JsonResponse({
            "message": f"Student {student_id} rented room {room_id} successfully"
        })
    return JsonResponse({"error": "Method not allowed"}, status=405)
