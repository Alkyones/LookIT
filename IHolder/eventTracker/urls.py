from django.urls import path
from . import views


urlpatterns = [
    path('', views.eventTrackerMain, name='event-main'),
    path('save/<str:eventName>/', views.saveEventToUser, name='save-event')
]