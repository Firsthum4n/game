from django.db import models
from django.utils import timezone


class Player(models.Model):
    username = models.CharField(max_length=50, unique=True)
    first_login = models.DateTimeField(null=True, blank=True)
    total_logins = models.PositiveIntegerField(default=0)
    last_login = models.DateTimeField(null=True, blank=True)
    points = models.IntegerField(default=0)

    def str(self):
        return self.username

    def daily_login(self):
        today = timezone.now().date()
        if self.last_login and self.last_login.date() == today:
            return False

        self.total_logins += 1
        self.last_login = timezone.now()
        if not self.first_login:
            self.first_login = timezone.now()
        self.points += 10
        self.save()
        return True


class BoostType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    def str(self):
        return self.name


class Boost(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    boost_type = models.ForeignKey(BoostType, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def str(self):
        return f"{self.boost_type.name} for {self.player.username}"

    def activate(self):
        """Активация буста."""
        self.start_date = timezone.now()
        self.save()

    def is_active(self):
        """Проверка, активен ли буст."""
        if self.start_date and self.end_date:
            return self.start_date <= timezone.now() <= self.end_date
        return False

