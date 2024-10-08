from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from blog.models import Post, Category, Tag
from .forms import *


class LoginTemplateView(LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomAuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect('app:index')


class RegisterTemplateView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('users:profile')  # Перенаправление после успешного обновления профиля
    login_url = '/users/login/'  # URL для перенаправления неаутентифицированных пользователей

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = Post.objects.order_by('-views')[:3]

        # Добавляем категории с подсчетом постов
        categories = Category.objects.annotate(post_count=Count('posts'))
        context['categories'] = categories
        context['tags'] = Tag.objects.all()
        return context
