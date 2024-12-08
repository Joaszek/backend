from django.core.management.base import BaseCommand
from django.db import connection
import os
import shutil
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from datetime import timedelta


class Command(BaseCommand):
    help = "Fully resets the database and populates initial data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting database reset process...")

        # Step 1: Drop the database schema
        self.reset_database()

        # Step 2: Delete all migration files
        self.delete_migration_files()

        # Step 3: Reapply migrations
        self.apply_migrations()

        # Step 4: Populate initial data
        self.create_initial_data()

        self.stdout.write("Database reset and initial data population completed successfully.")

    def reset_database(self):
        """
        Drops and recreates the database schema.
        """
        with connection.cursor() as cursor:
            self.stdout.write("Dropping and recreating the database schema...")
            cursor.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
        self.stdout.write("Database schema reset successfully.")

    def delete_migration_files(self):
        """
        Deletes all migration files from the project.
        """
        self.stdout.write("Deleting migration files...")
        for app_name in settings.INSTALLED_APPS:
            app_path = app_name.split(".")[0]
            migration_path = os.path.join(settings.BASE_DIR, app_path, "migrations")
            if os.path.exists(migration_path):
                for file_name in os.listdir(migration_path):
                    if file_name != "__init__.py" and file_name.endswith(".py"):
                        file_path = os.path.join(migration_path, file_name)
                        os.remove(file_path)
                        self.stdout.write(f"Deleted: {file_path}")
        self.stdout.write("Migration files deleted.")

    def apply_migrations(self):
        """
        Reapplies all migrations.
        """
        self.stdout.write("Applying migrations...")
        from django.core.management import call_command
        call_command("makemigrations")
        call_command("migrate", "--noinput")
        self.stdout.write("Migrations applied successfully.")

    def create_initial_data(self):
        """
        Populates initial data into the database.
        """
        self.stdout.write("Populating initial data...")
        from django.apps import apps

        # Get models dynamically
        Student = apps.get_model("Student", "Student")
        Admin = apps.get_model("Admin", "Admin")
        Faculty = apps.get_model("Faculty", "Faculty")
        Building = apps.get_model("Building", "Building")
        RoomToRent = apps.get_model("RoomToRent", "RoomToRent")
        RoomWithItems = apps.get_model("RoomWithItems", "RoomWithItems")
        Item = apps.get_model("Item", "Item")
        Booking = apps.get_model("Booking", "Booking")
        Attribute = apps.get_model("Attribute", "Attribute")
        Type = apps.get_model("Type", "Type")
        ItemBooking = apps.get_model("ItemBooking", "ItemBooking")

        # Create initial admin
        admin = Admin.objects.create(
            username="123456",
            password=make_password("admin123"),
            email="admin1@example.com",
            additional_field="Admin data",
            is_superuser=True,
            first_name="Adam",
            last_name="Kowalski",
            is_staff=True,
        )

        admin2 = Admin.objects.create(
            username="234567",
            password=make_password("admin123"),
            email="admin2@example.com",
            additional_field="Admin data",
            is_superuser=True,
            first_name="Adam",
            last_name="Kowalski",
            is_staff=False,
        )

        admin3 = Admin.objects.create(
            username="345678",
            password=make_password("admin123"),
            email="admin3@example.com",
            additional_field="Admin data",
            is_superuser=True,
            first_name="Adam",
            last_name="Nowak",
            is_staff=False,
        )
        admin4 = Admin.objects.create(
            username="456789",
            password=make_password("admin123"),
            email="admin4@example.com",
            additional_field="Admin data",
            is_superuser=True,
            first_name="Kuba",
            last_name="Kowalski",
            is_staff=False,
        )

        # Create initial faculty and building
        faculty = Faculty.objects.create(
            name="W04N",
            admin_id=admin.id,
        )

        faculty2 = Faculty.objects.create(
            name="W8",
            admin_id=admin2.id,
        )

        faculty3 = Faculty.objects.create(
            name="W1",
            admin_id=admin3.id,
        )

        facult4 = Faculty.objects.create(
            name="W12",
            admin_id=admin.id,
        )


        building11 = Building.objects.create(
            name="B1",
            faculty="W04N",
        )
        building12 = Building.objects.create(
            name="B2",
            faculty="W04N",
        )

        building21 = Building.objects.create(
            name="A1",
            faculty="W04N",
        )
        building22 = Building.objects.create(
            name="A2",
            faculty="W04N",
        )

        building31 = Building.objects.create(
            name="D1",
            faculty="W8",
        )
        building32 = Building.objects.create(
            name="D2",
            faculty="W12",
        )

        # Create rooms
        room_to_rent1 = RoomToRent.objects.create(
            room_number=102,
            building=building11.name,
            faculty=faculty.name,
            available=True,
        )

        room_to_rent2 = RoomToRent.objects.create(
            room_number=103,
            building=building12.name,
            faculty=faculty.name,
            available=False,
        )

        room_to_rent3 = RoomToRent.objects.create(
            room_number=104,
            building=building21.name,
            faculty=faculty.name,
            available=True,
        )

        room_to_rent4 = RoomToRent.objects.create(
            room_number=105,
            building=building21.name,
            faculty=faculty.name,
            available=True,
        )

        room_to_rent5 = RoomToRent.objects.create(
            room_number=106,
            building=building22.name,
            faculty=faculty.name,
            available=False,
        )

        room_to_rent6 = RoomToRent.objects.create(
            room_number=107,
            building=building31.name,
            faculty=faculty2.name,
            available=True,
        )

        room_to_rent7 = RoomToRent.objects.create(
            room_number=108,
            building=building32.name,
            faculty=faculty3.name,
            available=True,
        )

        room_to_rent8 = RoomToRent.objects.create(
            room_number=109,
            building=building31.name,
            faculty=faculty2.name,
            available=False,
        )

        room_to_rent9 = RoomToRent.objects.create(
            room_number=110,
            building=building32.name,
            faculty=faculty3.name,
            available=True,
        )

        room_to_rent10 = RoomToRent.objects.create(
            room_number=111,
            building=building12.name,
            faculty=faculty.name,
            available=False,
        )
        room_with_items1 = RoomWithItems.objects.create(
            room_number=103,
            faculty=faculty.name,
            building=building11.name,
        )

        room_with_items2 = RoomWithItems.objects.create(
            room_number=104,
            faculty=faculty.name,
            building=building12.name,
        )

        room_with_items3 = RoomWithItems.objects.create(
            room_number=105,
            faculty=faculty.name,
            building=building21.name,
        )

        room_with_items4 = RoomWithItems.objects.create(
            room_number=106,
            faculty=faculty.name,
            building=building21.name,
        )

        room_with_items5 = RoomWithItems.objects.create(
            room_number=107,
            faculty=faculty.name,
            building=building22.name,
        )

        room_with_items6 = RoomWithItems.objects.create(
            room_number=108,
            faculty=faculty2.name,
            building=building31.name,
        )

        room_with_items7 = RoomWithItems.objects.create(
            room_number=109,
            faculty=faculty3.name,
            building=building32.name,
        )

        room_with_items8 = RoomWithItems.objects.create(
            room_number=110,
            faculty=faculty2.name,
            building=building31.name,
        )

        room_with_items9 = RoomWithItems.objects.create(
            room_number=111,
            faculty=faculty3.name,
            building=building32.name,
        )

        room_with_items10 = RoomWithItems.objects.create(
            room_number=112,
            faculty=faculty.name,
            building=building12.name,
        )

        # Create student
        student = Student.objects.create(
            username="123456",
            password=make_password("student123"),
            email="student1@example.com",
            additional_field="Student data",
        )

        student2 = Student.objects.create(
            username="234567",
            password=make_password("student123"),
            email="student2@example.com",
            additional_field="Student data",
        )
        # Create student
        student3 = Student.objects.create(
            username="345678",
            password=make_password("student123"),
            email="student3@example.com",
            additional_field="Student data",
        )

        student4 = Student.objects.create(
            username="456789",
            password=make_password("student123"),
            email="student4@example.com",
            additional_field="Student data",
        )

        # Booking 1
        booking = Booking.objects.create(
            room_number=room_to_rent1.room_number,
            user=student.username,
            start_time=now().date(),
            end_time=now().date() + timedelta(days=7),
            building=building11.name,
            faculty=faculty.name,
        )

        # Booking 2
        booking2 = Booking.objects.create(
            room_number=room_to_rent2.room_number,
            user=student2.username,
            start_time=now().date(),
            end_time=now().date() + timedelta(days=7),
            building=building12.name,
            faculty=faculty.name,
        )

        # Booking 3
        booking3 = Booking.objects.create(
            room_number=room_to_rent3.room_number,
            user=student3.username,
            start_time=now().date(),
            end_time=now().date() + timedelta(days=7),
            building=building21.name,
            faculty=faculty.name,
        )

        # Booking 4
        booking4 = Booking.objects.create(
            room_number=room_to_rent6.room_number,
            user=student4.username,
            start_time=now().date(),
            end_time=now().date() + timedelta(days=7),
            building=building31.name,
            faculty=faculty2.name,
        )

        # Booking 5
        booking5 = Booking.objects.create(
            room_number=room_to_rent9.room_number,
            user=student.username,  # Same student to ensure only one booking per student
            start_time=now().date(),
            end_time=now().date() + timedelta(days=7),
            returned = True,
            building=building32.name,
            faculty=faculty3.name,
        )


        # Predefined types and attributes
        # Types
        types = ["Laptop", "Charger", "Mouse", "Keyboard", "Monitor", "Headphones", "Tablet", "Webcam", "Power Bank", "Hard Drive"]

        # Attributes
        attributes = ["Portable", "Charging", "Wireless", "Ergonomic", "Adjustable", "Noise Cancelling", "Touchscreen", "Compact", "Waterproof", "High-Speed"]


        for type_name in types:
            Type.objects.create(type_name=type_name)

        for attribute_name in attributes:
            Attribute.objects.create(attribute_name=attribute_name)

        # Create items
        items = [
            {"name": "Laptop 2", "amount": 5, "type": "Laptop", "attribute": "Portable", "room_number": "101", "building": building11.name, "faculty": faculty.name},
            {"name": "Charger 2", "amount": 10, "type": "Charger", "attribute": "Charging", "room_number": "102", "building": building12.name, "faculty": faculty.name},
            {"name": "Mouse 2", "amount": 8, "type": "Mouse", "attribute": "Wireless", "room_number": "103", "building": building21.name, "faculty": faculty.name},
            {"name": "Keyboard 1", "amount": 6, "type": "Keyboard", "attribute": "Ergonomic", "room_number": "104", "building": building21.name, "faculty": faculty.name},
            {"name": "Monitor 1", "amount": 4, "type": "Monitor", "attribute": "Adjustable", "room_number": "105", "building": building22.name, "faculty": faculty.name},
            {"name": "Headphones 1", "amount": 7, "type": "Headphones", "attribute": "Noise Cancelling", "room_number": "106", "building": building31.name, "faculty": faculty2.name},
            {"name": "Tablet 1", "amount": 5, "type": "Tablet", "attribute": "Touchscreen", "room_number": "107", "building": building31.name, "faculty": faculty2.name},
            {"name": "Webcam 1", "amount": 6, "type": "Webcam", "attribute": "Compact", "room_number": "108", "building": building32.name, "faculty": faculty3.name},
            {"name": "Power Bank 1", "amount": 9, "type": "Power Bank", "attribute": "Portable", "room_number": "109", "building": building32.name, "faculty": faculty3.name},
            {"name": "Hard Drive 1", "amount": 3, "type": "Hard Drive", "attribute": "High-Speed", "room_number": "110", "building": building12.name, "faculty": faculty.name},
        ]

        # Create items in the database
        for item_data in items:
            Item.objects.create(
                name=item_data["name"],
                amount=item_data["amount"],
                type=item_data["type"],
                attribute=item_data["attribute"],
                room_number=item_data["room_number"],
                building=item_data["building"],
                faculty=item_data["faculty"],
            )

        students = [student, student2, student3, student4]

        # Create item bookings
        for student in students:
            for item_data in items:
                if not ItemBooking.objects.filter(student_id=student.username, name=item_data["name"]).exists():
                    ItemBooking.objects.create(
                        item_id=item_data["name"],  # Using item name as the item_id here (adjust according to actual item_id field)
                        name=item_data["name"],
                        student_id=student.username,
                        start_date=now().date(),
                        end_date=now().date() + timedelta(days=5),
                    )

        self.stdout.write("Initial data population complete.")
