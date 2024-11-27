from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from datetime import timedelta

class Command(BaseCommand):
    help = "Resets the database and populates initial data"

    def handle(self, *args, **kwargs):
        # Step 1: Drop and recreate the database schema
        with connection.cursor() as cursor:
            self.stdout.write("Dropping and recreating the database schema...")
            cursor.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
        self.stdout.write("Database schema reset successfully.")

        # Step 2: Run migrations
        self.stdout.write("Applying migrations...")
        from django.core.management import call_command
        call_command("migrate", "--noinput")
        self.stdout.write("Migrations applied successfully.")

        # Step 3: Populate initial data
        self.stdout.write("Populating initial data...")
        self.create_initial_data()
        self.stdout.write("Initial data populated successfully.")

    from datetime import timedelta
    from django.utils.timezone import now
    from django.contrib.auth.hashers import make_password

    def create_initial_data(self):
        from django.apps import apps

        # Get the models dynamically
        Student = apps.get_model('Student', 'Student')
        Admin = apps.get_model('Admin', 'Admin')
        Faculty = apps.get_model('Faculty', 'Faculty')
        Building = apps.get_model('Building', 'Building')
        RoomToRent = apps.get_model('RoomToRent', 'RoomToRent')
        RoomWithItems = apps.get_model('RoomWithItems', 'RoomWithItems')
        Item = apps.get_model('Item', 'Item')
        Booking = apps.get_model('Booking', 'Booking')
        Attribute = apps.get_model('Attribute', 'Attribute')
        Type = apps.get_model('Type', 'Type')
        ItemBooking = apps.get_model('ItemBooking', 'ItemBooking')

        # Create initial Admin
        admin, _ = Admin.objects.get_or_create(
            username="123456",
            defaults={
                "password": make_password("admin123"),
                "email": "admin1@example.com",
                "additional_field": "Admin data",
                "is_superuser": True,
                "first_name": "Adam",
                "last_name": "Kowalski",
                "is_staff": True,
            },
        )

        # Create initial Faculty and Building
        faculty, _ = Faculty.objects.get_or_create(
            name="Engineering-Faculty",
            defaults={"admin_id": admin.id}
        )
        building, _ = Building.objects.get_or_create(
            name="B1",
            faculty='Engineering-Faculty'
        )

        # Create Rooms
        room_to_rent, _ = RoomToRent.objects.get_or_create(
            room_number=101,
            defaults={"building": building.name, "faculty": faculty.name}
        )
        room_with_items, _ = RoomWithItems.objects.get_or_create(
            room_number=102,
            defaults={"building": building.name}
        )

        # Create Student
        student, _ = Student.objects.get_or_create(
            username="123456",
            defaults={
                "password": make_password("student123"),
                "email": "student1@example.com",
                "additional_field": "Student data",
            },
        )

        # Create Booking
        Booking.objects.get_or_create(
            room_id=room_to_rent.room_to_rent_id,
            defaults={
                "user": student.username,
                "start_time": now().date(),
                "end_time": now().date() + timedelta(days=7),
                "building": building.name,
                "faculty": faculty.name,
            },
        )

        # Predefined Types and Attributes
        types = ["Laptop", "Charger", "Mouse"]
        attributes = ["Portable", "Charging", "Wireless"]

        # Create Types
        for type_name in types:
            Type.objects.get_or_create(type_name=type_name)

        # Create Attributes
        for attribute_name in attributes:
            Attribute.objects.get_or_create(attribute_name=attribute_name)

        # Create Items with a one-to-many relationship to RoomWithItems
        items = [
            {"name": "Laptop 1", "amount": 5, "type": "Laptop", "attribute": "Portable"},
            {"name": "Charger 1", "amount": 10, "type": "Charger", "attribute": "Charging"},
            {"name": "Mouse 1", "amount": 8, "type": "Mouse", "attribute": "Wireless"},
        ]

        created_items = []
        for item_data in items:
            item, _ = Item.objects.get_or_create(
                name=item_data["name"],
                defaults={
                    "amount": item_data["amount"],
                    "room_with_items": room_with_items.id,
                    "type": item_data["type"],
                    "attribute": item_data["attribute"],
                    "faculty": faculty.name,
                    "building": building.name,
                },
            )
            created_items.append(item)

        # Create ItemBooking data
        for item in created_items:
            ItemBooking.objects.get_or_create(
                item_id=item.item_id,
                defaults={
                    "student_id": student.username,
                    "start_date": now().date(),
                    "end_date": now().date() + timedelta(days=5),
                },
            )

        self.stdout.write("Initial data creation complete.")
