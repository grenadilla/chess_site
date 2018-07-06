from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('players/<user_name>', views.player, name='player'),
]
