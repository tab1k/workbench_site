from .views import *
from django.urls import path

app_name = 'app'

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
]
