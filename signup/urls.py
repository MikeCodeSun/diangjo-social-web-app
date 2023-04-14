from django.urls import path
from .views import login, signup, profile_list, profile,search_result



app_name = 'signup'

urlpatterns = [
  path('login/', login, name='login'),
  path('signup/', signup, name='signup'),
  path('profile_list/', profile_list, name='profile_list'),
  path("profile/<int:pk>", profile, name='profile'),
  path("search_result/", search_result, name='search_result'),
] 