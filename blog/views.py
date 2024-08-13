from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag, Comment
from .forms import CommentForm


# Представление для списка блогов
class BlogListView(ListView):
    context_object_name = 'blogs'
    paginate_by = 5  # Пагинация
    template_name = 'blog/blog.html'

    def get_queryset(self):
        # Аннотируем количество комментариев для каждого поста
        return Post.objects.filter(status='published').annotate(comment_count=Count('comments')).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = Post.objects.order_by('-views')[:3]

        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


class BlogDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object

        # Получаем популярные посты (например, топ-5 по количеству просмотров)
        context['popular_posts'] = Post.objects.order_by('-views')[:3]

        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['comment_count'] = self.object.comments.count()  # Количество комментариев текущего поста

        # Пагинация комментариев
        comments_list = self.object.comments.all().order_by('-created_at')  # Сортировка по дате создания в обратном порядке
        paginator = Paginator(comments_list, 3)  # Показываем 3 комментария на странице
        page_number = self.request.GET.get('page', 1)  # Получаем номер страницы из запроса
        page_obj = paginator.get_page(page_number)

        context['comments'] = page_obj
        return context


# Представление для блогов по категориям
class CategoryListView(ListView):
    template_name = 'blog/category_list.html'
    context_object_name = 'blogs'
    paginate_by = 5  # Пагинация

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return Post.objects.filter(category=self.category, status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

# Представление для блогов по тегам
class TagListView(ListView):
    template_name = 'blog/tag_list.html'
    context_object_name = 'blogs'
    paginate_by = 5  # Пагинация

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return Post.objects.filter(tags=self.tag, status='published').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


# Представление для добавления комментария к блогу
@login_required
def add_comment_to_blog(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Проверяем количество комментариев пользователя под этим постом
    user_comments_count = Comment.objects.filter(post=post, author=request.user).count()
    if user_comments_count >= 3:
        # Если пользователь написал уже 3 комментария, не позволяем добавить новый
        return render(request, 'blog/blog_detail.html', {
            'post': post,
            'form': CommentForm(),
            'error_message': 'Максимальное кол-во комментариев - 3, под постом.'
        })

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.email = request.user.email
            comment.save()
            return redirect('blog:blog-detail', slug=post.slug)
    else:
        form = CommentForm()

    return render(request, 'blog/blog_detail.html', {'post': post, 'form': form})
