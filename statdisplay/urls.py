from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('players', views.player_list, name='player_list'),
    path('players/<user_name>', views.players, name='players'),
    path('games', views.game_list, name='game_list'),
    path('games/<game_id>', views.games, name='games'),
    path('compare', views.compare, name='compare'),
]
