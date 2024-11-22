from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth.hashers import make_password


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

        # Create a default group (optional)
        Group = apps.get_model('auth', 'Group')
        default_group, _ = Group.objects.get_or_create(name="DefaultGroup")

        # Add a Student
        student, _ = Student.objects.get_or_create(
            username="student1",
            defaults={
                "password": make_password("password123"),
                "email": "student1@example.com",
                "additional_field": "Some additional data",
            }
        )

        # Add an Admin
        admin, _ = Admin.objects.get_or_create(
            username="admin1",
            defaults={
                "password": make_password("adminpassword123"),
                "email": "admin1@example.com",
                "additional_field": "Some admin data",
                "is_superuser": True
            }
        )

        self.stdout.write("Initial data creation complete.")
