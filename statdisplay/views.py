from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
from django.http import HttpResponse
from statdisplay.models import Player, Game
from .forms import CompareForm


def index(request):
    return HttpResponse("Hello, world. You're at the statdisplay index.")

def player_list(request):
    players = Player.objects.all().order_by('user_name')
    paginator = Paginator(players, 25)
    page = request.GET.get('page')
    players = paginator.get_page(page)
    context = {'players': players}
    return render(request, "statdisplay/player_list.html", context)

def players(request, user_name):
    player = Player.objects.filter(user_name__iexact=user_name).first()
    games = (Game.objects.filter(player_white=player) | 
            Game.objects.filter(player_black=player)).distinct().order_by('-date_finished')
    paginator = Paginator(games, 25)
    page = request.GET.get('page')
    games = paginator.get_page(page)
    context = {'player': player, 'games': games}
    return render(request, "statdisplay/player.html", context)

def game_list(request):
    games = Game.objects.all().order_by('-date_finished')
    paginator = Paginator(games, 25)
    page = request.GET.get('page')
    games = paginator.get_page(page)
    context = {'games': games}
    return render(request, "statdisplay/game_list.html", context)

def games(request, game_id):
    game = Game.objects.filter(game_id=game_id).first()
    context = {'game': game}
    return render(request, "statdisplay/game.html", context)

def compare(request):
    player1 = request.GET.get('player1')
    player2 = request.GET.get('player2')

    form = CompareForm(initial={'player1': player1, 'player2': player2})

    player1 = Player.objects.filter(user_name=player1).first()
    player2 = Player.objects.filter(user_name=player2).first()

    context = {'form': form, 'player1': player1, 'player2': player2}
    return render(request, "statdisplay/compare.html", context)
