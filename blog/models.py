from django.urls import reverse
from django.utils.text import slugify
from users.models import CustomUser
from django.conf import settings
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Название категории
    slug = models.SlugField(max_length=255, unique=True, blank=True)  # Для ЧПУ
    description = models.TextField(blank=True, null=True)  # Описание категории
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)  # Обработка кириллических символов
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']  # Сортировка по названию

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'slug': self.slug})  # URL для просмотра категории


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Название тега
    slug = models.SlugField(max_length=255, unique=True, blank=True)  # Для ЧПУ

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)  # Обработка кириллических символов
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']  # Сортировка по названию

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag_detail', kwargs={'slug': self.slug})  # URL для просмотра тегов


class Post(models.Model):
    title = models.CharField(max_length=200)  # Заголовок поста
    slug = models.SlugField(max_length=200, unique=True, blank=True)  # Для ЧПУ
    image = models.ImageField(upload_to='post/%Y/%m/%d', blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blog_posts')  # Автор поста
    content = models.TextField()  # Содержимое поста
    proverbs = models.TextField(max_length=500, blank=True, null=True)
    proverbs_author = models.CharField(max_length=255, blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='posts')  # Категория поста
    tags = models.ManyToManyField('Tag', related_name='posts')  # Теги поста
    created_at = models.DateTimeField(default=timezone.now)  # Дата создания
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего обновления
    status = models.CharField(max_length=10, choices=[('draft', 'Draft'), ('published', 'Published')], default='draft')
    views = models.PositiveIntegerField(default=0)

    def increment_views(self):
        self.views += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def show_tag(self):
        return ", ".join([tag.name for tag in self.tags.all()])

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # Пост, к которому относится комментарий
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')  # Автор комментария
    body = models.TextField()  # Содержимое комментария
    created_at = models.DateTimeField(default=timezone.now)  # Дата создания
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего обновления
    active = models.BooleanField(default=True)  # Флаг активности комментария

    class Meta:
        ordering = ['created_at']  # Сортировка по дате создания

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post}'