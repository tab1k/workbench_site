import requests
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from app.forms import QuoteForm
from blog.models import Post


class IndexTemplateView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = Post.objects.filter(status='published').order_by('-created_at')[:3]
        context['form'] = QuoteForm()
        return context

    def post(self, request, *args, **kwargs):
        form = QuoteForm(request.POST)
        if form.is_valid():
            # Получаем данные из формы
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            service = form.cleaned_data['service']
            message = form.cleaned_data['message']

            # Отправка данных в Telegram
            telegram_message = (
                f"Новое сообщение:\n"
                f"Имя: {name}\n"
                f"Email: {email}\n"
                f"Телефон: {phone}\n"
                f"Услуга: {service}\n"
                f"Сообщение: {message}"
            )

            # Замените <TELEGRAM_BOT_TOKEN> и <TELEGRAM_CHAT_ID> на ваши реальные данные
            bot_token = '6964008134:AAH4C4GD9_ya_SrAvamMiiTYiuPPetmrghc'
            chat_id = '-1002231337306'
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

            requests.post(url, data={'chat_id': chat_id, 'text': telegram_message})

            return self.render_to_response(self.get_context_data(success=True))

        return self.render_to_response(self.get_context_data(form=form))


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PortfolioView(TemplateView):
    template_name = 'portfolio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ContactsView(TemplateView):
    template_name = 'contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = QuoteForm()
        context['success'] = kwargs.get('success', False)
        return context

    def post(self, request, *args, **kwargs):
        form = QuoteForm(request.POST)
        if form.is_valid():
            # Получаем данные из формы
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            service = form.cleaned_data['service']
            message = form.cleaned_data['message']

            # Отправка данных в Telegram
            telegram_message = (
                f"Новое сообщение:\n"
                f"Имя: {name}\n"
                f"Email: {email}\n"
                f"Телефон: {phone}\n"
                f"Услуга: {service}\n"
                f"Сообщение: {message}"
            )

            # Замените <TELEGRAM_BOT_TOKEN> и <TELEGRAM_CHAT_ID> на ваши реальные данные
            bot_token = '6964008134:AAH4C4GD9_ya_SrAvamMiiTYiuPPetmrghc'
            chat_id = '-1002231337306'
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

            requests.post(url, data={'chat_id': chat_id, 'text': telegram_message})

            return self.render_to_response(self.get_context_data(success=True))

        return self.render_to_response(self.get_context_data(form=form))

def error_404_view(request, exception):
    return render(request, '404.html', status=404)