"""IHolder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from register import views as register_views
from Itracker.views import mainPage as baseView
from Itracker import views as itracker_views
from eventTracker import views as eventTracker_views

urlpatterns = [
    #system urls for admin and authendication
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('register/', register_views.register, name='register'),
    
    path('accounts/profile/', register_views.profile, name='profile'),
    path('accounts/profile/saved-news/', itracker_views.savedNews, name='saved-news'),
    path('accounts/profile/saved-news/share/<int:newId>/', itracker_views.savedNewShare, name='saved-news-share'),
    path('accounts/profile/saved-news/delete/<int:newId>/', itracker_views.savedNewDelete, name='saved-news-delete'),
    
    path('accounts/profile/saved-events/', eventTracker_views.savedUserEvents, name='saved-events'),
    path('accounts/profile/saved-events/share/<int:eventId>/', eventTracker_views.savedEventShare, name='saved-events-share'),
    path('accounts/profile/saved-news/delete/<int:eventId>/', eventTracker_views.savedEventDelete, name='saved-events-delete'),


    path('', baseView, name="Index_page"),
    #urls for the app
    path('accounts/Todo/', include('ToDo.urls')),
    path('accounts/Linksaver/', include('linksaver.urls')),
    path('accounts/EmailHandler/', include('emailrenderer.urls')), 
    path('Itracker/', include('Itracker.urls')),
    path('events/', include('eventTracker.urls')) 


]
