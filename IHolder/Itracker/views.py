from django.shortcuts import render, redirect
import requests

url = "https://bing-news-search1.p.rapidapi.com/news/search"

querystring = {"q":"Technology","setLang":"EN","freshness":"Day","count": 20,"originalImg": 'true',"textFormat":"Raw","safeSearch":"Off"}

headers = {
	"X-BingApis-SDK": "true",
	"X-RapidAPI-Key": "d1bb6976c6msh67c8d6e9e403942p1585cbjsn0254498457df",
	"X-RapidAPI-Host": "bing-news-search1.p.rapidapi.com"
}

# Create your views here.

def mainPage(request):
    if request.user.is_authenticated:
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        trendNews = (response['value'])
        return render(request, 'Itracker/index.html', context={'trendNews': trendNews})
    else:
        return redirect('/login')