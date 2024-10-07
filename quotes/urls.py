# quotes/urls.py

from django.urls import path
from . import views 

urlpatterns = [
    path('', views.quote, name='quote'),  # Main page with random quote
    path('show_all/', views.show_all, name='show_all'),  # Show all quotes
    path('about/', views.about, name='about'),  # About page
]