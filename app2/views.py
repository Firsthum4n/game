from .models import *

player1 = Player.objects.create(player_id = 1)
level1 = Level.objects.create(title='Уровень 1', order=1)
prize1 = Prize.objects.create(title='Золотой ключ')

player_level1 = PlayerLevel.objects.create(
    player=player1,
    level=level1,
    completed='2023-12-15',
    is_completed=True,
    score=100
)

assign_prize(player_level_id=player_level1.id, prize_id=prize1.id)

export_to_csv()

