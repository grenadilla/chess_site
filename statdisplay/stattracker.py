import os, sys
import requests, json, datetime
import django

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chess_site.settings")
django.setup()

from statdisplay.models import Player, Game

TEAM_NAME = "vhhs"

YESTERDAY = datetime.date.today() - datetime.timedelta(1)
YESTERDAY = datetime.datetime.combine(YESTERDAY, datetime.datetime.min.time())
EPOCH = datetime.datetime.utcfromtimestamp(0)
UNIX_TIME = int((YESTERDAY - EPOCH).total_seconds() * 1000.0)

print("Checking for new team members")
url = "https://lichess.org/team/" + TEAM_NAME + "/users"
resp = requests.get(url)
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
    url = ("https://lichess.org/api/games/user/" + 
           player.user_name + 
           "?moves=false&tags=false&since=" + 
           str(UNIX_TIME))
    print("Checking player " + player.user_name + " using url: " + url)
    resp = requests.get(url, headers={"Accept": "application/x-ndjson"})
    if resp.status_code == 200:
        print("Status code 200")
        print("Checking games")
        for line in resp.text.splitlines():
            data = json.loads(line)
            if "user" not in data["players"]["white"] or "user" not in data["players"]["black"]:
                continue
            if data["players"]["white"]["user"]["name"] == player.user_name:
                opponent_color = "black"
            else:
                opponent_color = "white"
            opponent = Player.objects.filter(user_name__iexact=data["players"][opponent_color]["user"]["name"])
            if not Game.objects.filter(game_id=data["id"]).exists() and opponent.exists():
                if opponent_color == "black":
                    white = player
                    black = opponent.first()
                else:
                    white = opponent.first()
                    black = player
                new_game = Game(game_id=data["id"], player_white=white, player_black=black)
                new_game.save()
                new_game.players.add(white)
                new_game.players.add(black)
                print("Added new game " + new_game.game_id)
print("Checking finished games")
for game in Game.objects.filter(complete=False):
    url = "https://lichess.org/api/game/" + game.game_id
    resp = requests.get(url)
    if resp.status_code == 200:
        print("Status code 200")
        data = resp.json()
        if not data["status"] == "started":
            game.complete = True
            if data["status"] == "draw":
                game.winner_id = 0
            elif "winner" in data and data["winner"] == "black":
                game.winner_id = 2
            elif "winner" in data and data["winner"] == "white":
                game.winner_id = 1
            game.save()
            print("Updated finished game " + game.game_id)
