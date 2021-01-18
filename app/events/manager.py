#import asyncio
import math
import callofduty
import json
from datetime import datetime
from callofduty import Mode, Platform, Title
from app.events.models import Event, Team, Match, Player
#from apscheduler.schedulers.asyncio import AsyncIOScheduler

num_teams = 23
num_players_per_team = 2
num_teams_per_division = 11

my_email = "johnny.lopez617@gmail.com"
my_password = "Saintviator1??"

#scheduler = AsyncIOScheduler()



def create_event():
    teams = []
    players = [Player(name="Johnny", username="oFewk#6235807"), Player(name="Tommy", username="tammy#9284071")]
    teams.append(Team(name="Johnny & Tommy", players=players))
    #for y in range(num_teams):
    #    players = []
    #    for x in range(num_players_per_team):
    #      players.append(Player("Player {}".format(x + y), "oFewk#6235807", x+y))
    #    teams.append(Team("Team {}".format(y), players))
    return Event(name="My Tournament", teams=teams, start_time=datetime.now(), end_time=datetime.now())

async def main():
    event = Event(name="test")#create_event()
    #print("Tournament has been created... {}".format(event))
    #event.seed_teams()
    #print("Divisions have been created... Num Divisions: {}".format(event.num_divisions))
    #await event.refresh_stats()
    event.save()
    #leaderboard = event.leaderboard
    #client = await callofduty.Login(my_email, my_password)

    #results = await client.SearchPlayers(Platform.Activision, "Captain Price", limit=3)
    #for player in results:
    #    print(f"{player.username} ({player.platform.name})")

    #me = results[1]
    #profile = await me.profile(Title.ModernWarfare, Mode.Multiplayer)

    #level = profile["level"]
    #kd = profile["lifetime"]["all"]["properties"]["kdRatio"]
    #wl = profile["lifetime"]["all"]["properties"]["wlRatio"]

    #print(f"\n{me.username} ({me.platform.name})")
    #print(f"Level: {level}, K/D Ratio: {kd}, W/L Ratio: {wl}")

#job = scheduler.add_job(main, 'interval', minutes=2)
#scheduler.start()
#print('Press Ctrl+{0} to exit'.format('C'))

# Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
#try:
#    asyncio.get_event_loop().run_forever()
#except (KeyboardInterrupt, SystemExit):
#    pass

#while True:
#    continue

#asyncio.get_event_loop().run_until_complete(main())
