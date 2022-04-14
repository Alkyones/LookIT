from django.urls import path
from . import views

urlpatterns = [
    path('lists/', views.UserLists, name='Lists'),
]