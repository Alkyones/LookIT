from django.urls import path
from . import views


urlpatterns = [
    path('', views.mainPage, name='baseMain'),
    path('<int:offset>/<int:limit>/', views.mainPage, name='base'),
    path('save/<str:name>/<int:page>', views.saveToProfile, name='save_to_profile'),
    path('share/<str:name>/<int:page>', views.shareUrl, name='share_url'),
    path('search/', views.searchNews, name='search_news'),
]