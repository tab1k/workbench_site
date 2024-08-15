from django.db import models
from users.models import CustomUser
from django.utils import timezone


class Game(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    coins = models.PositiveIntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)

    def add_coins(self, amount):
        self.coins += amount
        self.last_activity = timezone.now()
        self.save()


