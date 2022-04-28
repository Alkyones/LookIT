from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import newEmailForm
# Create your views here.

def new_email(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = newEmailForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                receiver = form.cleaned_data['email']
                send_mail(subject, message, settings.EMAIL_HOST_USER, [receiver], fail_silently=False)
                redirect('emailrenderer')
        form = newEmailForm()
        return render(request, 'emailrenderer/emailrenderer.html', {'form': form})
    else:
        return redirect('/login')
        