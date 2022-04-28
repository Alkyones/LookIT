from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import newEmailForm
# Create your views here.

def send_email(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = newEmailForm(request.POST)
            if form.is_valid():
                pass
        
        form = newEmailForm()
        return render(request, 'emailrenderer/emailrenderer.html', {'form': form})
    else:
        return redirect('/login')
        