from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserLists, name='Lists'),
]