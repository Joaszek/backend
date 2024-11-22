"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from backendApp.Admin.views import login
from backendApp.Student.views import student_login
urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/login', student_login, name='student-login'),
    path('admin1/login', login, name='login'),
    path('student/', include('backendApp.Student.urls')),  # Include Student app routes
    path('admin/', include('backendApp.Admin.urls')),      # Include Admin app routes
]
