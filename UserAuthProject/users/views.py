# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)  # Print form errors to the console for debugging
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def dashboard_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'user_type'):
            user_type = request.user.user_type
            if user_type == 'doctor':
                return render(request, 'users/doctor_dashboard.html', {'user': request.user})
            elif user_type == 'patient':
                return render(request, 'users/patient_dashboard.html', {'user': request.user})
        else:
            # Handle case where user_type is not defined (e.g., default behavior)
            return HttpResponse("User type not defined.")
    return redirect('login')  # Redirect to login if user is not authenticated
