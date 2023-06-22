from serpapi import GoogleSearch
from django.shortcuts import redirect, render
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from Itracker.forms import searchForm 
from .models import SavedEvents, searchSavedEvents, userSavedEventsModel
from django.contrib import messages
import time



def eventTrackerMain(request):
    savedUserEvents = userSavedEventsModel.objects.filter(user=request.user).values_list("title", flat=True)
    if request.method == 'POST':
        form = searchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data['searchQuery']
            if not q : q = 'world' # default if needed
            query = "Technology events in " + q
            params = {
            "api_key": "f3a475f6e29e497877e080689748bc0fe45ac40a573a1e775da3679a8634f183",
            "engine": "google_events",
            "q": query,
            "google_domain": "google.com",
            "hl": "en",
            "gl": "us"
                }
            search = GoogleSearch(params)
            results = search.get_dict()
            if 'events_results' in results.keys():
                results = results['events_results']
                for event in results:
                    if 'description' not in event.keys():
                        desc = 'No description available'
                    else:
                        desc = event['description']
                    title=event['title']
                    if not title: title = 'No title available'
                    
                    eventDate=event['date']['when']
                    if not eventDate: eventDate = 'No data'
                    link=event['link']
                    if not link : link = 'No Link'
                    item = searchSavedEvents(title=title,description= desc, eventDate=eventDate, link=link)
                    item.save()
            else:
                messages.warning(request,'There is no upcoming events for three months period.')

            form = searchForm()

            return render(request, 'eventTracker/search.html', {'events': results,'savedEvents':savedUserEvents, 'form': form})

    else:
        form = searchForm()
        lastEventsAll = SavedEvents.objects.filter().order_by('-id')[:30][::-1]
        lastTenEvents,lastEventsAll = lastEventsAll[:10], lastEventsAll[10:]
        return render(request, 'eventTracker/index.html', {'lastEvents': lastTenEvents,'lastEventsAll':lastEventsAll,'savedNews':savedUserEvents, 'form': form})

def saveEventToUser(request,eventName):
    find_event = searchSavedEvents.objects.filter(title=eventName)[:1]
    if find_event:
        for event in find_event:
            title = event.title
            desc = event.description
            eventDate = event.eventDate
            link = event.link  
            # request.usersavedeventsmodel_set.create(title = title,desccription = desc,eventDate = eventDate,link = link)
            item = userSavedEventsModel.objects.create(title=title, description=desc, eventDate=eventDate, link=link, user=request.user)
            item.save()

    form = searchForm()
    lastEventsAll = searchSavedEvents.objects.filter().order_by('-id')[:20][::-1]
    lastTenEvents,lastEventsAll = lastEventsAll[:10], lastEventsAll[10:]

    savedUserEvents = userSavedEventsModel.objects.filter(user=request.user).values_list("title", flat=True)


    return render(request, 'eventTracker/search.html', {'events': lastTenEvents,'lastEventsAll':lastEventsAll,'savedEvents':savedUserEvents, 'form': form})
    
def savedUserEvents(request):
    if request.user.is_authenticated:
        savedUserEvents = userSavedEventsModel.objects.filter(user=request.user)
        if savedUserEvents:
            return render(request, 'eventTracker/savedEvents.html', {'savedEvents': savedUserEvents})
        else:
            messages.success(request, 'No events can be found please try again later.')
            return render(request, 'eventTracker/savedEvents.html')


def savedEventDelete(request, id):
    if id:
        new = userSavedEventsModel.objects.get(id=id)
        new.delete()
        messages.success(request, 'Removed from profile!')
    return redirect('/accounts/profile/saved-news')

def eventCrawler():
    options = Options()
    options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
    options.add_argument("--headless")

    url = "https://www.eventbrite.com/d/online/all-events/"
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(2)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    newsToSave = []
    listNews = soup.find('div', {'class':'search-results-panel-content'}).find('ul', {"class": "search-main-content__events-list"}).find_all('li')
    for li in listNews:
        newObj = {}
        sectionTitleInfo = li.find('section')
        ps = sectionTitleInfo.find_all("p", {"class": "Typography_align-match-parent__4bejd"})
        print(ps)
        if sectionTitleInfo:
            print(sectionTitleInfo)
            link = sectionTitleInfo.find("a")["href"]
            title = sectionTitleInfo.find("h2").text
            eventDate = ps[0].text
            publisher = "No Publisher"
        
            img = sectionTitleInfo.find('img')
            if img : img = img['src']
            else: img = 'not found'
        
            newObj['link'] = link
            newObj['title'] = title
            newObj['image'] = img
            newObj['timeEvent'] = eventDate
            newObj['publisher'] = publisher
            newsToSave.append(newObj)
        for item in newsToSave:
            so = SavedEvents.objects.create(**item)
            print(so)
            so.save()
    return


def savedEventShare(request, id):
    pass

# eventCrawler()