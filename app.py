import json, os
from quart import Quart, render_template, websocket, request, jsonify

app = Quart(__name__)

my_email = os.environ.get('EMAIL')
my_password = os.environ.get('PASSWORD')


@app.route("/stats", methods=['GET'])
async def stats():
    try:
        username = request.args.get('username')
        client = await callofduty.Login(my_email, my_password)
        matches = await get_recent_matches_for_player(client, username)
        #matches = json.dumps([match.__dict__ for match in matches])
        #match = matches[0]
        matches_json = []
        for match in matches:
            matches_json.append(match)
        #print(matches)
        return {"matches": matches_json}
    except:
        return {}

#import asyncio
import callofduty
from callofduty import Mode, Platform, Title

my_email = "johnny.lopez617@gmail.com"
my_password = "Saintviator1??"

#scheduler = AsyncIOScheduler()

async def get_recent_matches_for_player(client, username, startTimestamp=None, endTimestamp=None):
    if username is None:
        return

    #todo add timestamps
    startTimestamp = None

    player = (await client.SearchPlayers(Platform.Activision, username, limit=1))[0]
    recent_matches = await player.matches(Title.ModernWarfare, Mode.Warzone)
    #return recent_matches
    matches = []
    #all_matches = []
    for match in recent_matches:
        cur_match_data = await client.GetFullMatch(Platform.Activision, Title.ModernWarfare, Mode.Warzone, match.id)
        match_data = json.dumps(cur_match_data)
        matches.append(match_data)
    return matches
    #return recent_matches

async def get_matches_for_team(team, startTimestamp=None, endTimestamp=None, mode="br_brduos"):
    print("Getting matches for team {}".format(team))
    client = await callofduty.Login(my_email, my_password)
    player_ids = []
    for player in team.players:
        results = await client.SearchPlayers(Platform.Activision, player.username, limit=1)
        if len(results) > 0:
            player_ids.append(results[0].accountId)
    if len(player_ids) != len(team.players):
        # TODO - add exception
        return

    usernames = ['oFewk', 'tammy'] #[player.username for player in team.players]
    matches = (await get_recent_matches_for_player(client, team.players[0], startTimestamp=startTimestamp, endTimestamp=endTimestamp))
    team_matches = []
    print("Received {} possible matches".format(len(matches)))
    for match in matches:
        match_data = await client.GetFullMatch(Platform.Activision, Title.ModernWarfare, Mode.Warzone, match.id)
        match_data = json.dumps(match_data)
        match_data = json.loads(match_data)
        if match_data['allPlayers'][0]['mode'] != mode:
            continue

        all_players = match_data['allPlayers']
        possible_players = []
        team_names = []
        for player in all_players:
            #print(player)
            player_info = player['player']
            username = player_info['username']
            player_id = player_info['uno']
            team_name = player_info['team']
            #print("{} in {}: {}".format(player_id, player_ids, player_id in player_ids))
            for id in player_ids:
                if int(id) - int(player_id) == 0:
                    #print("testing...")
                    possible_players.append(player)
                    team_names.append(team_name)
                    break

        valid_players = []
        valid_player_stats = []
        for team_name in team_names:
            valid_player_count = 0
            valid_matches = []
            for player in possible_players:
                if player['player']['team'] == team_name:
                    valid_players.append(player)
            if len(valid_players) == len(team.players):
                #print(json.dumps(valid_players, indent=10))

                valid_player_stats = valid_players
                break

        team_matches.append({
            "id": match.id,
            "stats": valid_player_stats
        })
    return team_matches

if __name__ == "__main__":
    app.run()
