from django.urls import path
from . import views


urlpatterns = [
    path('', views.new_email, name='emailrenderer'),
]