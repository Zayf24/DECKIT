from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        # Use Django's built-in AuthenticationForm for validation
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            # Authenticate the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Log the user in
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')  # Redirect to the home page or dashboard
            else:
                # Authentication failed
                messages.error(request, 'Invalid username or password.')
        else:
            # Form validation failed
            messages.error(request, 'Please correct the errors below.')
    else:
        # Display the login form for GET requests
        form = AuthenticationForm()
    
    return render(request, 'user/login.html', {'form': form})

def user_home(request):
    # Only authenticated users should access this page
    if request.user.is_authenticated:
        return render(request, 'user/home.html')
    else:
        return redirect('login')
    
def hero(request):
    return render(request, 'user/hero.html')