from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('chat/', login_required(views.chat), name='chat'),
    path('chat/<int:itemId>', login_required(views.searchItem), name='searchItem'),

]
