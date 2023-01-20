from django.shortcuts import render, redirect

# Create your views here.

def mainPage(request):
    if request.user.is_authenticated:
        return render(request, 'base.html')
    else:
        return redirect('/login')