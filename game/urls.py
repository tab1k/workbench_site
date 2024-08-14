from django.urls import path
from .views import *

app_name = 'game'

urlpatterns = [
    path('', GameView.as_view(), name='index'),
    path('complete-task/', CompleteTaskView.as_view(), name='complete_task'),
]
