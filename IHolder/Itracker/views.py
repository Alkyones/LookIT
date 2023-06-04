from django.shortcuts import render, redirect
from django.contrib import messages
from .models import newsModel, userSavedNewsModel
from .forms import searchForm
import requests
import pyperclip


searchUrl = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/search/NewsSearchAPI"
#! prod 'X-RapidAPI-Key': 'd1bb6976c6msh67c8d6e9e403942p1585cbjsn0254498457df',
#!      'X-RapidAPI-Host': 'contextualwebsearch-websearch-v1.p.rapidapi.com'
headers = {
    "X-RapidAPI-Key": "716d4828fdmshdeb8bfb4916b0a1p14be71jsn4d10fe6a76c7",
    "X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com"
}



def mainPage(request):
    if request.user.is_authenticated:
        form = searchForm()

        page = 1
        pageCount = 10
        pageOffset = 0
        pagereq = request.GET.get("page")
        if pagereq :
            page = int(pagereq)
            pageCount = page * 10
            pageOffset = pageCount - 10
        
        paramSearch = request.GET.get("q")
        searchQuery = "Technology"
        if paramSearch:
            searchQuery = paramSearch

        savedNews = newsModel.objects.all()
        savedNews = list(savedNews)
       
        querystring = {"q":searchQuery,"pageNumber":"1","pageSize":"20","autoCorrect":"true","fromPublishedDate":"null","toPublishedDate":"null"}
        response = requests.request("GET", searchUrl, headers=headers, params=querystring).json()
        if 'error' in response.keys():
            print("Error")
            trendNews = savedNews
            trendNews = savedNews[:20:-1]
        else:
            trendNews = response['value']
        return render(request, 'Itracker/index.html', context={'trendNews': trendNews, 'savedNews': savedNews, 'page': page, "form":form, 'query':searchQuery})
    else:
        return redirect('/login')

def searchNews(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = searchForm(request.POST)
            if form.is_valid():
                searchQuery = form.cleaned_data['searchQuery']

                page = 1
                pageCount = 10
                pageOffset = 0


                querystring = {"q":searchQuery,"pageNumber":"1","pageSize":"50","autoCorrect":"true","fromPublishedDate":"null","toPublishedDate":"null"}
                response = requests.request("GET", searchUrl, headers=headers, params=querystring).json()
                trendNews = (response['value'])
        
                savedNews = newsModel.objects.values_list("title", flat=True)
                savedNews = list(savedNews)
                form = searchForm()

        return render(request, 'Itracker/index.html', context={'trendNews': trendNews, 'savedNews': savedNews, 'page': page,'form':form, 'query':searchQuery})
    else:
        return redirect('/login')

def saveToProfile(request, name, page):
    if request.user.is_authenticated:
        name.replace('%20', ' ')
        querystring = {"q":name, "pageNumber":"1","pageSize":"1","autoCorrect":"true","fromPublishedDate":"null","toPublishedDate":"null"}
        response = requests.request("GET", searchUrl, headers=headers, params=querystring).json()
        if 'error' in response.keys():
            filtered_item = newsModel.objects.filter(title=name)[:1]
            if filtered_item:
                newName = filtered_item[0].title
                newDesc = filtered_item[0].description
                newUrl = filtered_item[0].url
                newImage = filtered_item[0].image
        elif response['value'][0]:
            new = response['value'][0]
            newName = new['title']
            newDesc = new['description']
            newUrl = new['url']
            
            if 'image' in new.keys():
                if new['image']['url'] :
                    newImage = new['image']['url']
                else:
                    newImage = 'not found'
            else:
                newImage = 'not found'

        # elif response['value'][0]:
        #     new = response['value'][0]
        #     newName = new['name']
        #     newDesc = new['description']
        #     newUrl = new['url']
            
        #     if 'image' in new.keys():
        #         if new['image']['contentUrl'] :
        #             newImage = new['image']['contentUrl']
        #         else:
        #             newImage = 'not found'
        #     else:
        #         newImage = 'not found'
        request.user.usersavednewsmodel_set.create(
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


def savedNews(request):
    if request.user.is_authenticated:
        savedNews = userSavedNewsModel.objects.filter(user=request.user)
        return render(request, 'Itracker/savedNews.html',context={'savedNews':savedNews})
    else:
        return redirect('/login')

def savedNewDelete(request,newId):
    if newId:
        new = userSavedNewsModel.objects.get(id=newId)
        new.delete()
        messages.success(request, 'Removed from profile!')
    return redirect('/accounts/profile/saved-news')

def savedNewShare(request,newId):
    if newId:
        new = userSavedNewsModel.objects.get(id=newId)
        if new:
            pyperclip.copy(new.url)
            messages.success(request, 'Copied to clipboard')
        else:
            messages.success(request, 'Failed to copy')
    return redirect('/accounts/profile/saved-news')


def searchNewsLocation(request):
    if request.method == 'POST':
        form = searchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['searchQuery']
            url = "https://real-time-news-data.p.rapidapi.com/local-headlines"

            querystring = {"query":query,"lang":"en"}
            #! prod 'X-RapidAPI-Key': 'd1bb6976c6msh67c8d6e9e403942p1585cbjsn0254498457df',
            #!      'X-RapidAPI-Host': 'real-time-news-data.p.rapidapi.com'
            headers = {
                "X-RapidAPI-Key": "716d4828fdmshdeb8bfb4916b0a1p14be71jsn4d10fe6a76c7",
                "X-RapidAPI-Host": "real-time-news-data.p.rapidapi.com"
            }

            response = requests.request("GET", url, headers=headers, params=querystring).json()
            if 'data' in response.keys():
                savedNews = response['data']
            else:
                savedNews = []
                messages.success(request, f"No news found nearby {query}")
            return render(request, 'Itracker/newsLocation.html', {'form': form, 'savedNews': savedNews})
            
    else:
        form = searchForm();
        return render(request, 'Itracker/newsLocation.html', {'form': form})

# Crawlers / spiders

def scrapFromWeb( query):
    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/search/NewsSearchAPI"

    querystring = {"q":query,"pageNumber":"1","pageSize":"50","autoCorrect":"true","fromPublishedDate":"null","toPublishedDate":"null"}
    #! prod 'X-RapidAPI-Key': 'd1bb6976c6msh67c8d6e9e403942p1585cbjsn0254498457df',
    #!      'X-RapidAPI-Host': 'contextualwebsearch-websearch-v1.p.rapidapi.com'
    headers = {
        "X-RapidAPI-Key": "716d4828fdmshdeb8bfb4916b0a1p14be71jsn4d10fe6a76c7",
        "X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring).json()

    if 'error' not in response.keys():
        news= response['value']

        for new in news:
            title,descr,url,image = '', '', '', ''
            if new['title']:
                title = new['title']
            if new['description']:
                descr = new['description']
            if new['url']:
                url = new['url']
            if new['image']:
                image = new['image']['url']
            item = newsModel.objects.create(title=title, description=descr, image=image, url=url)
            item.save()
    return

def scrapERT(query="technology"):
    searchUrl = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/search/NewsSearchAPI"
    headers = {
        "X-RapidAPI-Key": "716d4828fdmshdeb8bfb4916b0a1p14be71jsn4d10fe6a76c7",
        "X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com"
    }
    querystring = {"q":query,"pageNumber":"1","pageSize":"50","autoCorrect":"true","fromPublishedDate":"null","toPublishedDate":"null"}
    response = requests.request("GET", searchUrl, headers=headers, params=querystring).json()
    if 'error' not in response.keys():
        trendNews= response['value']
        if trendNews:
            for new in trendNews:
                newName = new['title']
                newDesc = new['description']
                newUrl = new['url']
                
                if 'image' in new.keys():
                    if new['image']['url'] :
                        newImage = new['image']['url']
                    else:
                        newImage = 'not found'
                else:
                    newImage = 'not found'

                item = newsModel.objects.create(
                url = newUrl,
                title = newName,
                description = newDesc,
                image = newImage)
                item.save()
        return
    
# scrapFromWeb("Technology")
# scrapERT("Technology")