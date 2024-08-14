from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Game


class GameView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        # Используем select_related, если Game связан с User через ForeignKey
        try:
            game = Game.objects.select_related('user').get(user=user)
            coins = game.coins
            registration_date = user.registration_date
        except Game.DoesNotExist:
            coins = 0
            registration_date = None

        max_value = 100000000  # Максимальное значение (100,000,000 койнов)
        min_display = 0.01 * max_value
        normalized_coins_percent = max(min((coins - min_display) / (max_value - min_display) * 99 + 1, 100), 1)

        formatted_registration_date = registration_date.isoformat() if registration_date else None

        return render(request, 'game/index.html', {
            'coins': coins,
            'normalized_coins_percent': normalized_coins_percent,
            'registration_date': formatted_registration_date
        })


class CompleteTaskView(LoginRequiredMixin, View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'User not authenticated'}, status=403)

        try:
            game, created = Game.objects.get_or_create(user=user)

            if created:
                print(f"Created new Game record for user {user.username}")

            game.add_coins(1)
            return JsonResponse({'success': True, 'coins': game.coins})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)