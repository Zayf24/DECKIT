from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from flashcard.models import Deck

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

@login_required
def user_home(request):
    # Only authenticated users should access this page
    recent_decks = None
    if request.user.is_authenticated:
        recent_decks = Deck.objects.filter(
            user=request.user,
            last_accessed__isnull=False
        ).order_by('-last_accessed')[:3]

        popular_decks = Deck.objects.all().order_by('-views')[:4]
    return render(request, 'user/home.html', {'recent_decks': recent_decks,'popular_decks':popular_decks})
    
def hero(request):
    return render(request, 'user/hero.html')

@login_required
def profile(request):
    # The user is available in request.user
    return render(request, 'user/profile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('hero') 