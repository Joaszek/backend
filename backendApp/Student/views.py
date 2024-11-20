from django.contrib.auth import authenticate, login
from django.http import JsonResponse

def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"}, status=200)
        return JsonResponse({"error": "Invalid credentials"}, status=401)
    return JsonResponse({"error": "Invalid method"}, status=405)
