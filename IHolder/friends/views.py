from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Friends

# Create your views here.
def add_friend(request):
    userFriends = Friends.objects.filter(user=request.user)
    allUsers = User.objects.filter(user=request.user.username)
    return redirect(request.META.get('HTTP_REFERER'))

def search_friend(request):
    pass

def remove_friend(request):
    pass

def friends(request):
    if request.user.is_authenticated:
        userFriends = Friends.objects.filter(user=request.user)
        return render(request, 'friends/friends.html', {'userFriends': userFriends})


def send_message(request):
    pass