from django.shortcuts import redirect, render
from .models import linksModel
from .forms import linksForm, linkEditForm

# crud linksaver


def linksaverIndex(request):
    if request.method == 'POST':
        form = linksForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            request.user.linksmodel_set.create(
                url=data['url'], title=data['title'])

    form = linksForm()
    links = request.user.linksmodel_set.all() # save and insert 
    context = {
        'form': form,
        'links': links,
    }
    return render(request, 'linksaver/index.html', context)

def linksaverDelete(request, id):
    link = linksModel.objects.get(id=id)
    link.delete()
    return redirect('index')

def linksaverEdit(request, id):
    link = linksModel.objects.get(id=id)
    if request.method == 'POST':
        form = linkEditForm(request.POST, instance=link)
        if form.is_valid():
            form.save()
            return redirect('index')
    form = linkEditForm(instance=link)
    context = {
        'form': form,
        'link': link,
    }
    return render(request, 'linksaver/url_edit.html', context)
