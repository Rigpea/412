#mini_fb views.py 


from django.shortcuts import render
from .models import Profile, StatusMessage, Image
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
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
class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        # Back to profile
        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})
    
class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'  

    def get_success_url(self):
        # go back to profile
        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})
class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'  # The template to render the form

    def get_success_url(self):
        # Redirect back to the profile page after updating
        return reverse('show_profile', kwargs={'pk': self.object.pk})

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
        sm = form.save(commit=False)
        sm.profile = profile  
        sm.save()

        # Getting and processing the uploaded images
        files = self.request.FILES.getlist('files') 
        
        for file in files:
        
            img = Image()
            img.image_file = file  
            img.status_message = sm  # image has a reference to a status_message
            img.save()  # put inmage in database
        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']}) 
