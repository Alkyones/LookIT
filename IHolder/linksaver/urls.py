from django.urls import path
from . import views


urlpatterns = [
    path('', views.linksaverIndex, name='index'),
    path('delete/<int:id>', views.linksaverDelete, name='delete'),
    path('edit/<int:id>', views.linksaverEdit, name='edit'),
]