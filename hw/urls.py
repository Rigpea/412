## hw/urls.py
## description: the app-specific URLS for the hw application
from django.urls import path
from django.conf import settings
from . import views

#create a l

urlpatterns = [
    path(r'', views.home, name="home"), ## our first URL on the app hte main page
]