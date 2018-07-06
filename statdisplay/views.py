from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from statdisplay.models import Player, Game


def index(request):
    return HttpResponse("Hello, world. You're at the statdisplay index.")

def player(request, user_name):
    player = Player.objects.filter(user_name__iexact=user_name).first()
    games = (Game.objects.filter(player_white=player) | Game.objects.filter(player_black=player)).distinct()
    context = {'player': player, 'games': games}
    return render(request, "statdisplay/player.html", context)
