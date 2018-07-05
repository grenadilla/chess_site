import os, sys
import requests, json
import django

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chess_site.settings")
django.setup()

from statdisplay.models import Player, Game

TEAM_NAME = "vhhs"
print("Checking for new team members")
resp = requests.get("https://lichess.org/team/" + TEAM_NAME + "/users")
if resp.status_code == 200:
    print("Status code 200")
    for line in resp.text.splitlines():
        data = json.loads(line)
        if not Player.objects.filter(user_name__iexact=data["username"]).exists():
            if "profile" not in data:
                new_player = Player(user_name=data["username"], first_name="placeholder", last_name="placeholder")
            else:
                first_name = data["profile"]["firstName"]
                last_name = data["profile"]["lastName"]
                new_player = Player(user_name=data["username"], 
                                    first_name=first_name, 
                                    last_name=last_name,
                                    email=first_name.lower() + "." + last_name.lower() + "@vhhscougars.org")
            new_player.save()
            print("Added new player " + new_player.user_name)

for player in Player.objects.all():
    print("Checking player " + player.user_name)
    resp = requests.get("https://lichess.org/api/user/" + player.user_name + "/activity")
    if resp.status_code == 200:
        print("Status code 200")
        data = resp.json()
        if "correspondenceMoves" in data[0]:
            print("Checking games")
            for game in data[0]["correspondenceMoves"]["games"]:
                opponent = Player.objects.filter(user_name__iexact=game["opponent"]["user"])
                if not Game.objects.filter(game_id=game["id"]).exists() and opponent.exists():
                    if game["color"] == "white":
                        white = player
                        black = opponent.first()
                    else:
                        white = opponent.first()
                        black = player
                    new_game = Game(game_id=game["id"], player_white=white, player_black=black)
                    new_game.save()
                    new_game.players.add(white)
                    new_game.players.add(black)
                    print("Added new game " + new_game.game_id)
        if "correspondenceEnds" in data[0]:
            print("Checking finished games")
            for game in data[0]["correspondenceEnds"]["games"]:
                resp = requests.get("https://lichess.org/api/game/" + game["id"])
                if resp.status_code == 200:
                    print("Status code 200")
                    data = resp.json()
                    game_object = Game.objects.filter(game_id=data["id"]).first()
                    if not game_object.complete:
                        game_object.complete = True
                        if data["winner"] == "white":
                            game_object.winner_id = 1
                        elif data["winner"] == "black":
                            game_object.winner_id = 2
                        else:
                            game_object.winner_id = 0
                        game_object.save()
                        print("Updated finished game " + game_object.game_id)
