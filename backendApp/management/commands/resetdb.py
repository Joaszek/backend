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

        # Create initial faculty and building
        faculty = Faculty.objects.create(
            name="Engineering-Faculty",
            admin_id=admin.id,
        )
        building = Building.objects.create(
            name="B1",
            faculty="Engineering-Faculty",
        )

        # Create rooms
        room_to_rent = RoomToRent.objects.create(
            room_number=101,
            building=building.name,
            faculty=faculty.name,
        )
        room_with_items = RoomWithItems.objects.create(
            room_number=102,
            building=building.name,
        )

        # Create student
        student = Student.objects.create(
            username="123456",
            password=make_password("student123"),
            email="student1@example.com",
            additional_field="Student data",
        )

        # Create booking
        Booking.objects.create(
            room_number=room_to_rent.room_number,
            user=student.username,
            start_time=now().date(),
            end_time=now().date() + timedelta(days=7),
            building=building.name,
            faculty=faculty.name,
        )

        # Predefined types and attributes
        types = ["Laptop", "Charger", "Mouse"]
        attributes = ["Portable", "Charging", "Wireless"]

        for type_name in types:
            Type.objects.create(type_name=type_name)

        for attribute_name in attributes:
            Attribute.objects.create(attribute_name=attribute_name)

        # Create items
        items = [
            {"name": "Laptop 1", "amount": 5, "type": "Laptop", "attribute": "Portable"},
            {"name": "Charger 1", "amount": 10, "type": "Charger", "attribute": "Charging"},
            {"name": "Mouse 1", "amount": 8, "type": "Mouse", "attribute": "Wireless"},
        ]

        created_items = []
        for item_data in items:
            item = Item.objects.create(
                name=item_data["name"],
                amount=item_data["amount"],
                room_number=room_with_items.room_number,
                type=item_data["type"],
                attribute=item_data["attribute"],
                faculty=faculty.name,
                building=building.name,
            )
            created_items.append(item)

        # Create item bookings
        for item in created_items:
            ItemBooking.objects.create(
                item_id=item.item_id,
                student_id=student.username,
                start_date=now().date(),
                end_date=now().date() + timedelta(days=5),
            )

        self.stdout.write("Initial data population complete.")
