from django.urls import path
from .views import ShowAllProfilesView, ShowProfilesPageView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilesPageView.as_view(), name='show_profile'),

]