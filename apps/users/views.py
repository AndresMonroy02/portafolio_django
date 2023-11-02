from django.shortcuts import render
from .models import User
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        # Get the user data from the request
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        # Create a new user
        user = User.objects.create_user(username, username, password)
        user.save()
        # Log the user in after registration
        login(request, user)
        return redirect('dashboard')  # Replace 'success_page' with the actual URL for a successful registration

    return render(request, 'register.html')


def login_view(request):
    data = request.GET
    url = 'dashboard'
    print(data)

    if 'next' in data and data['next'] != '':
        url = data['next']
    print(url)


    if request.method == 'POST':
        email = request.POST['email']  # Change 'username' to 'email'
        password = request.POST['password']
        print(email)

        user = authenticate(username=email, password=password)  # Authenticate with email

        if user is not None:
            login(request, user)
            return redirect(url)  # Replace 'dashboard' with the URL name of your dashboard view
        else:
            print("No estás logeado")  # Handle login failure

    return render(request, 'registration/login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')