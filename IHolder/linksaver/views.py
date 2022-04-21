from django.shortcuts import render

# Create your views here.
def linksaverIndex(request):
    return render(request, 'linksaver/index.html')