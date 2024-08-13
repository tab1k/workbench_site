from .views import *
from django.contrib.auth.views import LogoutView
from django.urls import path

app_name = 'blog'


urlpatterns = [
    path('', BlogListView.as_view(), name='blog-list'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category-list'),
    path('tag/<slug:slug>/', TagListView.as_view(), name='tag-list'),
    path('<slug:slug>/comment/', add_comment_to_blog, name='add-comment-to-blog'),
]