from django.db import models

# Create your models here.
class Player(models.Model):
    user_name = models.CharField(max_length=32)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.CharField(max_length=64, null=True)
    rating = models.IntegerField(default=1500)

    def __str__(self):
        return self.user_name

class Game(models.Model):
    game_id = models.CharField(max_length=32)
    players = models.ManyToManyField(Player, related_name="games")
    player_white = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="white_games")
    player_black = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="black_names")
    winner_id = models.IntegerField(default=0)
    # 0 is draw, 1 is white, 2 is black
    complete = models.BooleanField(default=False)

    def __str__(self):
        return "Game: " + self.game_id
