from django.shortcuts import render, redirect
from django.contrib import messages
from .models import newsModel
import requests
import pyperclip


# Create your views here.
searchUrl = "https://bing-news-search1.p.rapidapi.com/news/search"
headers = {
    "X-BingApis-SDK": "true",
    "X-RapidAPI-Key": "d1bb6976c6msh67c8d6e9e403942p1585cbjsn0254498457df",
    "X-RapidAPI-Host": "bing-news-search1.p.rapidapi.com"
}


def mainPage(request):
    if request.user.is_authenticated:
        page = 1
        pageCount = 10
        pageOffset = 0
        pagereq = request.GET.get("page")
        if pagereq :
            page = int(pagereq)
            pageCount = page * 10
            pageOffset = pageCount - 10
        querystring = {"q":"Technology","setLang":"EN","freshness":"Day","count": pageCount, "offset": pageOffset ,"originalImg": 'true',"textFormat":"Raw","safeSearch":"Off"}
        response = requests.request("GET", searchUrl, headers=headers, params=querystring).json()
        trendNews = (response['value'])
        # trendNews = []
        
        savedNews = newsModel.objects.values_list("title", flat=True)
        savedNews = list(savedNews)
        
        return render(request, 'Itracker/index.html', context={'trendNews': trendNews, 'savedNews': savedNews, 'page': page})
    else:
        return redirect('/login')

def saveToProfile(request, name, page):
    if request.user.is_authenticated:
        querystring = {"q":name,"setLang":"EN","count": 1,"originalImg": 'true',"textFormat":"Raw","safeSearch":"Off"}
        response = requests.request("GET", searchUrl, headers=headers, params=querystring).json()
        if response['value'][0]:
            new = response['value'][0]
            newName = new['name']
            newDesc = new['description']
            newUrl = new['url']
            
            if 'image' in new.keys():
                if new['image']['contentUrl'] :
                    newImage = new['image']['contentUrl']
                else:
                    newImage = 'not found'
            else:
                newImage = 'not found'
            request.user.newsmodel_set.create(
                url = newUrl,
                title = newName,
                description = newDesc,
                image = newImage,
            )
        return redirect(f'/?page={page}')

def shareUrl(request,name,page):
    querystring = {"q":name,"setLang":"EN","count": 1,"originalImg": 'true',"textFormat":"Raw","safeSearch":"Off"}
    response = requests.request("GET", searchUrl, headers=headers, params=querystring).json()
    if response['value'][0]:
        new = response['value'][0]
        pyperclip.copy(new['url'])
        messages.success(request, 'Copied to clipboard')
    return redirect(f'/?page={page}')