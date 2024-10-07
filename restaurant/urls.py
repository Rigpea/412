# quotes/urls.py

from django.urls import path
from . import views 

urlpatterns = [
    path('main/', views.main, name='main'),  # Main page with random quote
    path('order/', views.order, name='order'),  # Show all quotes
    path('confirmation/', views.confirmation, name='confirmation'),
    #path('about/', views.about, name='about'),  # About page
]