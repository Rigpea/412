#mini_fb views.py 


from django.shortcuts import render
from .models import Profile, StatusMessage
from django.views.generic import ListView, DetailView, CreateView
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

    # gotta now pass it the profile how? 
    # need to perform a get operatino from model 

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context = {
            'profile': profile,
            'form': self.get_form(self.form_class)
        }
        return context
    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']}) 
