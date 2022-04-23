from django.shortcuts import render
from .models import linksModel
from .forms import linksForm

# crud linksaver
def linksaverIndex(request):
    if request.method == 'POST':
        form = linksForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            request.user.linksmodel.create(data)
    form = linksForm()
    links = request.user.linksmodel_set.all()
    context = {
        'form': form,
        'links': links,
    }
    return render(request, 'linksaver/index.html', context)