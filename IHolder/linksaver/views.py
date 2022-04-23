from django.shortcuts import render

# crud linksaver
def linksaverIndex(request):
    return render(request, 'linksaver/index.html')