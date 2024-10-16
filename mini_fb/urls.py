from django.urls import path
from .views import ShowAllProfilesView, ShowProfilesPageView, CreateProfileView, CreateStatusMessageView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilesPageView.as_view(), name='show_profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/create_status',CreateStatusMessageView.as_view(), name='create_status')

]