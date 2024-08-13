from django import forms
from .models import Comment
from .models import Category, Tag


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
