from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserLists, name='Lists'),
    path('<int:listId>/', views.ListItems, name='ListItems'),
    path('<int:listId>/delete/', views.DeleteList, name='DeleteList'),
    path('<int:listId>/<int:ItemId>/', views.ListItemsUpdate, name='ItemDetails'),
    path('<int:listId>/<int:ItemId>/delete/', views.ListItemsDelete, name='ItemDelete'),

]