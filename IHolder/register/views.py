from django.shortcuts import render,redirect
from .forms import NewRegisterForm
from django.contrib import messages





# Create your views here.
def register(request):
    if request.method == 'POST':
        form = NewRegisterForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, 'Form is not valid')
    else:
        form = NewRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def profile(request):
    if request.user.is_authenticated:
        return render(request, 'registration/profile.html')
    else:
        redirect('/login')