#mini_fb views.py 


from django.shortcuts import render
from .models import Profile
from django.views.generic import ListView, DetailView

# Create your views here.

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

# Thiw view needs to obtain data for one profile record, and 
#to deleguate work to a templaete called 
#show_profile.htlm to display that profile needs to render
class ShowProfilesPageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profiles'  # or 'profile'
    

    # gotta now pass it the profile how? 
    # need to perform a get operatino from model 

