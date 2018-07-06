from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('players/<user_name>', views.players, name='players'),
    path('games/<game_id>', views.games, name='games'),
]
