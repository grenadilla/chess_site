from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the statdisplay index.")

def player(request, user_id):
    context = {'id': user_id}
    return render(request, "statdisplay/player.html", context)
