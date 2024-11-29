import logging

from django.contrib.auth import authenticate, login
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from backendApp.Booking.models import Booking
from backendApp.Item.models import Item
from backendApp.ItemBooking.models import ItemBooking
from backendApp.RoomToRent.models import RoomToRent
from django.http import JsonResponse
import json

logger = logging.getLogger(__name__)


@csrf_exempt
def student_login(request):
    """
    Handle student login.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.debug(f"Received data: {data}")
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
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


@csrf_exempt
def get_available_rooms(request, username):
    """
    Fetch all RoomToRent objects from the database.
    If the student has reservations, return an empty list.
    """
    if request.method == "GET":
        try:
            emptyRooms = RoomToRent.objects.filter(available=True)
            if len(emptyRooms) == 0:
                return JsonResponse({"rooms": []}, status=200)

            # Fetch all RoomToRent objects
            room_list = [
                {
                    "id": room.id,
                    "room_number": room.room_number,
                    "building": room.building,
                    "faculty": room.faculty,
                    "is_to_rent": room.is_to_rent,
                    "available": room.available,
                }
                for room in emptyRooms
            ]
            return JsonResponse({"rooms": room_list}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def get_available_items(request, id):
    """
    Fetch available items for students.
    """
    if request.method == "GET":
        try:
            student_id = id
            if not student_id:
                return JsonResponse({"error": "student_id is required"}, status=400)

            items = Item.objects.filter(amount__gt=0)
            logger.debug(f"Items: {items}")
            item_list = []

            for item in items:
                is_booked = ItemBooking.objects.filter(item_id=item.item_id, student_id=student_id).exists()
                if not is_booked:
                    logger.debug(f"Item {item.item_id} is available")
                    item_list.append({
                        "id": item.item_id,
                        "name": item.name,
                        "amount": item.amount,
                        "room_number": item.room_number,
                        "type": item.type,
                        "attribute": item.attribute,
                        "building": item.building,
                        "faculty": item.faculty
                    })

            return JsonResponse({"items": item_list}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def rent_item(request):
    """
    Allow students to rent an item.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
            item_id = data.get('item_id')
            start_date = data.get('start_date')
            end_date = data.get('end_date')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Validate that the item exists and has a positive amount
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)

        if item.amount <= 0:
            return JsonResponse({"error": "Item is not available for rent"}, status=400)

        # Check if the student has already rented the same item
        existing_rentals = ItemBooking.objects.filter(item_id=item_id, user_id=student_id)
        if existing_rentals.exists():
            return JsonResponse({"error": "Item already rented by the student"}, status=400)

        # Decrement the item amount
        item.amount -= 1
        item.save()

        # Create a new ItemBooking
        ItemBooking.objects.create(
            item_id=item_id,
            user_id=student_id,
            start_date=start_date,
            end_date=end_date
        )

        return JsonResponse({
            "message": f"Student {student_id} rented item {item_id} successfully"
        }, status=201)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def rent_room(request):
    """
    Allow students to rent a room.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
            room_id = data.get('room_id')
            start_date = data.get('start_date')
            end_date = data.get('end_date')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Validate that the room exists
        try:
            room = RoomToRent.objects.get(id=room_id)
        except RoomToRent.DoesNotExist:
            return JsonResponse({"error": "Room not found"}, status=404)

        # Check if the room is already rented
        if Booking.objects.filter(room_to_rent=room).exists():
            return JsonResponse({"error": "Room is already rented"}, status=400)

        # Check if the student has already rented a room
        if Booking.objects.filter(user_id=student_id).exists():
            return JsonResponse({"error": "Student has already rented a room"}, status=400)

        # Create a new Booking
        Booking.objects.create(
            room_to_rent=room,
            user_id=student_id,
            start_time=start_date,
            end_time=end_date
        )

        return JsonResponse({
            "message": f"Student {student_id} rented room {room_id} successfully"
        }, status=201)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def get_reserved_items(request, username):
    """
    Fetch reserved items for a specific student by username.
    """
    if request.method == "GET":
        items = ItemBooking.objects.filter(user__username=username).select_related('item')
        item_list = [
            {
                "id": item.id,
                "name": item.item_id,
                "student_id": item.student_id,
                "start_date": item.start_date,
                "end_date": item.end_date,
                "attribute": item.returned,
            }
            for item in items
        ]
        return JsonResponse({"items": item_list}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def get_reserved_rooms(request, username):
    """
    Fetch reserved rooms for a specific student by username.
    """
    if request.method == "GET":
        # rooms = Booking.objects.filter(user=username && returned=False)
        # room_list = [
        #     {
        #         "id": room.id,
        #         "room_number": room.room_number,
        #         "building": room.building,
        #         "faculty": room.faculty,
        #         "start_date": room.start_time,
        #         "end_date": room.end_time
        #     }
        #     for room in rooms
        # ]
        # return JsonResponse({"rooms": room_list}, status=200)
        return JsonResponse({"rooms": []}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)
