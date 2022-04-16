from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserLists, name='Lists'),
    path('<int:listId>/', views.ListItems, name='ListItems'),
]