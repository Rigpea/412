#mini_fb views.py 


from django.shortcuts import render
from .models import Profile, StatusMessage, Image
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.urls import reverse
import logging
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

logger = logging.getLogger(__name__)

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
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        # Back to profile
        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})
    
    
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'  

    def get_success_url(self):
        # go back to profile
        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})
class UpdateProfileView(LoginRequiredMixin, UpdateView):
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
    
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context
    def form_valid(self, form):
        try:
            profile = Profile.objects.get(pk=self.kwargs['pk'])
            sm = form.save(commit=False)
            sm.profile = profile
            sm.save()

            # Debugging: check retrieved files
            files = self.request.FILES.getlist('files')
            print("Files retrieved:", files)
            
            for file in files:
                print("Saving file:", file)
                img = Image()
                img.image_file = file
                img.status_message = sm
                img.save()

            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error creating status message: {e}")
            form.add_error(None, "An unexpected error occurred in form_valid")
            return self.form_invalid(form)
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        other = Profile.objects.get(pk=self.kwargs['other_pk'])
        profile.add_friend(other)

        return HttpResponseRedirect(reverse('show_profile', kwargs={'pk': profile.pk}))
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profiles'

class ShowNewsFeedView(DetailView): # should I show to any 
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profiles'

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
