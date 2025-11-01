
from django.contrib.auth.models import User
from background_task import background
from TWhelper.parsers.json_parser import JsonParser
from TWhelper.bot.swgohlib.experience_api_client import ExperienceAPIClient
from background_task.models_completed import CompletedTask
from datetime import timedelta
import json
import requests


# Updates database every ***(period of time)
@background(schedule=2)
def update_db(user, ally_code):
    """
        !!! Saca json !!!
    """
    url = "https://swgoh-stat-calc.glitch.me/api?flags=calcGP"
    client = ExperienceAPIClient()

    print("\nFetching information for %s:" % user)

    # Get first from Swgoh.help.api
    rooster = client.get_player_roster(ally_code)

    # Pass the previous json to crinolo api for stats calculations
    rooster_stats = requests.post(url=url, data=json.dumps(rooster), headers={
                                  'Content-type': 'application/json'})

    rooster_stats = rooster_stats.json()

    """
    filename = "TWhelper/json_repo/" + str(user) + ".json"

    with open(filename, "w") as outfile:
        json.dump(rooster_stats, outfile)
    """
    print("Updating database for %s..." % user)

    JsonParser.parse_player_roster_to_db(rooster_stats, user, ally_code)


@background(schedule=2)
def update_guild_members():
    """
        Description:
    """
    # Delete all completed tasks, so as to not hording too much information
    CompletedTask.objects.all().delete()

    # Update game unit list
    client = ExperienceAPIClient()
    ZeSabre_ally_code = "189762389"

    """
        TODO: Meter a info do game unit num json mais pequeno...
    """
    print("Fetching game units info...")
    game_units = client.get_game_units()
    with open("TWhelper/json_repo/game_units.json", "w") as outfile:
        json.dump(game_units, outfile)

    # Update guild members
    print("\nFetching guild members info...")
    guild_players = client.get_guild_players(ZeSabre_ally_code)
    with open('TWhelper/json_repo/guild_players.json', 'w') as outfile:
        json.dump(guild_players, outfile)

    with open("TWhelper/json_repo/guild_players.json", "r") as src_file:
        json_data = json.load(src_file)

    players = User.objects.all()
    # Get list of player's usernames out of query into a simple list
    players_list = [x.first_name if x.first_name is not '' else x.username for x in players]
    minutes_counter = 0
    minutes_increment = 20

    for player in json_data[0]['roster']:
        if player['name'] in players_list:
            print('detected: ', player['name'])
            minutes_counter += minutes_increment
            update_db(player['name'], player['allyCode'],
                      schedule=timedelta(minutes=minutes_counter))

    # Close cycle with new task so that it keeps repeating
    update_guild_members(schedule=timedelta(hours=17))
    """

    """
