from django.db import models
import csv


class Player(models.Model):
    player_id = models.CharField(max_length=100)


class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)


class Prize(models.Model):
    title = models.CharField(max_length=100)


class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField()
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)


class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField()

def assign_prize(player_level_id, prize_id):
    try:


        player_level = PlayerLevel.objects.get(pk=player_level_id)
        prize = Prize.objects.get(pk=prize_id)
        if not LevelPrize.objects.filter(level=player_level.level, prize=prize).exists():
            LevelPrize.objects.create(
                level=player_level.level,
                prize=prize,
                received=player_level.completed
            )
            print(f"Приз {prize.title} присвоен игроку за уровень {player_level.level.title}.")
        else:
            print(f"Приз {prize.title} уже присвоен за уровень {player_level.level.title}.")

    except PlayerLevel.DoesNotExist:
        print(f"PlayerLevel с ID {player_level_id} не найден.")
    except Prize.DoesNotExist:
        print(f"Prize с ID {prize_id} не найден.")


def export_to_csv(filename='player_levels_data.csv'):

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID игрока', 'Название уровня', 'Пройден', 'Полученный приз'])
        for player_level in PlayerLevel.objects.all():
            prize_title = LevelPrize.objects.filter(level=player_level.level).values_list('prize__title', flat=True).first()
            writer.writerow([
                player_level.player.player_id,
                player_level.level.title,
                'Да' if player_level.is_completed else 'Нет',
                prize_title if prize_title else ''
            ])
        print(f"Данные экспортированы в файл {filename}.")