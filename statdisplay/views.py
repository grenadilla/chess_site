from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from statdisplay.models import Player, Game


def index(request):
    return HttpResponse("Hello, world. You're at the statdisplay index.")

def player_list(request):
    players = Player.objects.all().order_by('user_name')
    context = {'players': players}
    return render(request, "statdisplay/player_list.html", context)

def players(request, user_name):
    player = Player.objects.filter(user_name__iexact=user_name).first()
    games = (Game.objects.filter(player_white=player) | 
            Game.objects.filter(player_black=player)).distinct().order_by('-date_finished')
    context = {'player': player, 'games': games}
    return render(request, "statdisplay/player.html", context)

def game_list(request):
    games = Game.objects.all().order_by('-date_finished')
    context = {'games': games}
    return render(request, "statdisplay/game_list.html", context)

def games(request, game_id):
    game = Game.objects.filter(game_id=game_id).first()
    context = {'game': game}
    return render(request, "statdisplay/game.html", context)
