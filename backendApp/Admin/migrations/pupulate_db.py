from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_initial_data(apps, schema_editor):
    print("Starting initial data")

    # Get the Student model (custom user model) and Admin model
    Student = apps.get_model('Student', 'Student')
    Admin = apps.get_model('Admin', 'Admin')

    # Create a default group
    Group = apps.get_model('auth', 'Group')
    default_group, _ = Group.objects.get_or_create(name="DefaultGroup")

    # Create default permission
    Permission = apps.get_model('auth', 'Permission')
    default_permission, _ = Permission.objects.get_or_create(
        name="Can add log entry",
        codename="add_logentry",
        content_type_id=1  # Adjust this if the content type is different in your database
    )

    # Add a Student
    student, _ = Student.objects.get_or_create(
        username="student1",
        defaults={
            "password": make_password("password123"),
            "email": "student1@example.com",
            "additional_field": "Some additional data"
        }
    )
    student.groups.add(default_group)
    student.user_permissions.add(default_permission)

    # Add an Admin
    admin, _ = Admin.objects.get_or_create(
        username="admin1",
        defaults={
            "password": make_password("adminpassword123"),
            "email": "admin1@example.com",
            "additional_field": "Some admin data"
        }
    )
    admin.groups.add(default_group)
    admin.user_permissions.add(default_permission)

    print("Finished initial data")


def reverse_initial_data(apps, schema_editor):
    # Reverse data creation for clean rollback
    Student = apps.get_model('Student', 'Student')
    Admin = apps.get_model('Admin', 'Admin')
    Student.objects.filter(username="student1").delete()
    Admin.objects.filter(username="admin1").delete()


class Migration(migrations.Migration):
    dependencies = [
        ('Admin', '0001_initial'),  # Ensure this matches your initial migration file
        ('Student', '0001_initial'),  # Ensure this matches your initial migration file
    ]

    operations = [
        migrations.RunPython(create_initial_data, reverse_initial_data),
    ]
