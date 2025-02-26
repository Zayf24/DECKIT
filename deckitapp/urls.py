"""
URL configuration for deckitapp project.

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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import user.views as user_views
import flashcard.views as flashcard_views

urlpatterns = [
    path('',user_views.hero,name='hero'),
    path('admin/', admin.site.urls),
    path('signup/',user_views.signup,name='signup'),
    path('login/',user_views.user_login,name='login'),
    path('profile/', user_views.profile, name='profile'),
    path('home/',user_views.user_home,name='home'),
    path('create/', flashcard_views.create_deck, name='create_deck'),
    path('decks/', flashcard_views.deck_list, name='deck_list'),
    path('deck/<int:deck_id>/', flashcard_views.deck_detail, name='deck_detail'),
    path('search/', flashcard_views.search_decks, name='search_decks'),
    path('logout/',user_views.logout_view, name='logout'),
] 

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
