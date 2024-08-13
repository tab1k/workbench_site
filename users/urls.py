from .views import *
from django.contrib.auth.views import LogoutView
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('login/', LoginTemplateView.as_view(), name='login'),
    path('register/', RegisterTemplateView.as_view(), name='register'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
]
