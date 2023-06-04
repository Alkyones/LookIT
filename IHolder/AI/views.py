from django.shortcuts import render
from selenium import webdriver
from bs4 import BeautifulSoup
from .models import AIChatModelNew
from django.contrib.auth.decorators import login_required
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import undetected_chromedriver as uc
import json

from django.db import models
from django.contrib.auth.models import User



@login_required
def chat(request):
    options = webdriver.ChromeOptions() 
    options.add_argument('--user-data-dir=C:\\Users\\lifeo\\AppData\\Local\\Google\\Chrome')
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    userSearches = AIChatModelNew.objects.filter(user=request.user)
    if request.method == 'POST':
        keyword = request.POST['keyword']
        user = request.user  
        
        keyword = keyword.replace(' ', '+') # url conversion
        driver.get(f'https://www.bing.com/search?q={keyword}&count=50')
        keyword = keyword.replace('+', ' ')

        
        myElem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'b_results')))
        print("page ready")
        all_li = BeautifulSoup(driver.page_source, 'lxml')
        all_li = all_li.find("ol", {"id":"b_results"})
        all_li = all_li.find_all("li", {"class":"b_algo"})
        links = ""
        count = 0
        for li in all_li:
            titleDiv = li.find("h2")
            a = titleDiv.find("a")
            a = a['href']
            title = titleDiv.text
            print(title)
            
            item = str(title) +  " ### " + str(a)

            links += f"{item}\n"

        result = AIChatModelNew(keyword= keyword, links= links, user= user)
        result.save()
        userSearches = AIChatModelNew.objects.filter(user=request.user)
        return render(request, 'ai/chat.html', {'result': userSearches})
    else:
        return render(request, 'ai/chat.html', {'result': userSearches})
    

def searchItem(request, itemId):
    userSearches = AIChatModelNew.objects.filter(user=request.user, id=itemId);
    item = userSearches[0]
    itemLinks = item.links.split('\n')
    itemNewlinks = []

    for link in itemLinks:
        element = link.split('###')
        try:
            title = element[0]
            link = element[1]
            pushItem = {"title": title, "link": link}
            itemNewlinks.append(pushItem)
        except: pass

    return render(request, 'ai/searchItem.html', {'item': item, 'itemLinks': itemNewlinks})