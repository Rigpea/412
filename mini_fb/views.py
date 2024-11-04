#mini_fb views.py 


from django.shortcuts import render
from .models import Profile, StatusMessage, Image
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.urls import reverse
import logging
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

logger = logging.getLogger(__name__)

# Create your views here.

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_profile = self.request.user.profiles.first()
            context['user_profile'] = self.request.user.profiles.first()
            if user_profile:
                context['user_profile_pk'] = user_profile.pk
            return context

#show_profile.htlm to display that profile needs to render
class ShowProfilesPageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profiles'  # or 'profile'

    def get_object(self):
        use = self.request.user
        pk = self.kwargs.get('pk')
        prof = Profile.objects.filter(user=use).first()

        if use.is_authenticated and pk == prof.pk: 
            if pk == prof.pk: 
                return prof
        else: 
            return super().get_object()



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

    def get_login_url(self) -> str:
        return reverse('login') 

    def get_success_url(self):
        # Back to profile
        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})
    
    
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'  
    def get_login_url(self) -> str: 
        return reverse('login') 

    def get_success_url(self):
        # go back to profile
        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'  # The template to render the form
    
    def get_object(self):
        use = self.request.user
        prof = Profile.objects.filter(user=use).first()
        if prof: 
            return prof
        
    def get_login_url(self) -> str:
        return reverse('login') 
    def get_success_url(self):
        # Redirect back to the profile page after updating
        return reverse('show_profile', kwargs={'pk': self.object.pk})
class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    def get_context_data(self, **kwargs: any):
        context = super().get_context_data(**kwargs)
        if 'create_user_form' not in context:
            context['create_user_form'] = UserCreationForm()
        return context
    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            form.instance.user = user 
            #login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    def get_login_url(self) -> str:
        return reverse('login') 
    
    def get_context_data(self):
        context = super().get_context_data() 
        use = self.request.user
        profile = Profile.objects.get(user=use)
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        try:
            use = self.request.user
            profile = Profile.objects.get(user=use)
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
        use = self.request.user
        profile = Profile.objects.filter(user=use).first()
        pk = profile.pk
        return reverse('show_profile', kwargs={'pk': pk})
class CreateFriendView(LoginRequiredMixin, View):
    def get_login_url(self) -> str:
        return reverse('login') 
    def dispatch(self, request, *args, **kwargs):
        use = self.request.user
        profile = Profile.objects.filter(user=use).first()
        other = Profile.objects.get(pk=self.kwargs['other_pk'])
        profile.add_friend(other)
        
        return HttpResponseRedirect(reverse('show_profile', kwargs={'pk': profile.pk}))
    def get_object(self):
        use = self.request.user
        prof = Profile.objects.filter(user=use).first()
        if prof: 
            return prof

        
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profiles'
    def get_object(self):
        use = self.request.user
        prof = Profile.objects.filter(user=use).first()
        if prof: 
            return prof
    def get_login_url(self) -> str:

        return reverse('login') 

class ShowNewsFeedView(LoginRequiredMixin, DetailView): # should I show to any 
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profiles'

    def get_object(self):
        use = self.request.user
        prof = Profile.objects.filter(user=use).first()
        
        if prof: 
            return prof
        else:
            raise Http404("Profile Not found")
    def get_login_url(self):
        return reverse('login')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    def get_login_url(self) -> str:

        return reverse('login') 
    model = Profile
