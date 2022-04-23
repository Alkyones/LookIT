from django.shortcuts import redirect, render
from .models import linksModel
from .forms import linksForm

# crud linksaver


def linksaverIndex(request):
    if request.method == 'POST':
        form = linksForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            request.user.linksmodel_set.create(
                url=data['url'], title=data['title'], description=data['description'])

    form = linksForm()
    links = request.user.linksmodel_set.all()
    context = {
        'form': form,
        'links': links,
    }
    return render(request, 'linksaver/index.html', context)

def linksaverDelete(request, id):
    link = linksModel.objects.get(id=id)
    link.delete()
    return redirect('index')