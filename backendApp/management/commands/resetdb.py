from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now, timedelta


class Command(BaseCommand):
    help = "Resets the database and populates initial data"

    def handle(self, *args, **kwargs):
        # Step 1: Reset the database
        with connection.cursor() as cursor:
            self.stdout.write("Dropping and recreating database schema...")
            cursor.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
        self.stdout.write("Database schema reset successfully.")

        # Step 2: Apply migrations
        self.stdout.write("Applying migrations...")
        from django.core.management import call_command
        call_command("migrate")
        self.stdout.write("Migrations applied successfully.")

        # Step 3: Populate initial data
        self.stdout.write("Populating initial data...")
        self.create_initial_data()
        self.stdout.write("Initial data populated successfully.")

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
        ItemBooking = apps.get_model('ItemBooking', 'ItemBooking')
        Booking = apps.get_model('Booking', 'Booking')
        Type = apps.get_model('Type', 'Type')
        Attribute = apps.get_model('Attribute', 'Attribute')

        # Create initial Faculty and Building
        admin, _ = Admin.objects.get_or_create(
            username="123456",
            defaults={
                "password": make_password("admin123"),
                "email": "admin1@example.com",
                "additional_field": "Admin data",
                "is_superuser": True,
            },
        )
        faculty = Faculty.objects.create(name="Engineering Faculty", admin=admin)
        building = Building.objects.create(name="B1", faculty=faculty)

        # Create Rooms
        room_to_rent = RoomToRent.objects.create(room_number=101, building=building)
        room_with_items = RoomWithItems.objects.create(room_number=102, building=building)

        # Create Users
        student, _ = Student.objects.get_or_create(
            username="123456",
            defaults={
                "password": make_password("student123"),
                "email": "student1@example.com",
                "additional_field": "Student data",
            },
        )

        # Create Bookings
        Booking.objects.create(room_to_rent=room_to_rent, user=student, start_time=now().date(), end_time=now().date() + timedelta(days=7))

        # Create Types and Attributes
        # laptop_type, _ = Type.objects.get_or_create(type_name="Laptop")
        # charger_type, _ = Type.objects.get_or_create(type_name="Charger")
        # mouse_type, _ = Type.objects.get_or_create(type_name="Mouse")
        #
        # laptop_attribute, _ = Attribute.objects.get_or_create(attribute_name="Portable")
        # charger_attribute, _ = Attribute.objects.get_or_create(attribute_name="Charging")
        # mouse_attribute, _ = Attribute.objects.get_or_create(attribute_name="Wireless")
        #
        # # Create Items
        # Item.objects.create(
        #     name="Laptop 1", amount=5, room_with_items=room_with_items, type=laptop_type, attribute=laptop_attribute
        # )
        # Item.objects.create(
        #     name="Charger 1", amount=10, room_with_items=room_with_items, type=charger_type, attribute=charger_attribute
        # )
        # Item.objects.create(
        #     name="Mouse 1", amount=8, room_with_items=room_with_items, type=mouse_type, attribute=mouse_attribute
        # )

        self.stdout.write("Initial data creation complete.")
