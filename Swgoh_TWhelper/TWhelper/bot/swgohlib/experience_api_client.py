from TWhelper.bot.swgohlib.swgoh_api_client import Credentials
from TWhelper.bot.swgohlib.swgoh_api_client import SwgohHelperClient
# import swapi


class ExperienceAPIClient:
    """
    Experience API will provide the essentials, user friendly.
    """

    def __init__(self):
        __credentials = Credentials("MightyPython", "E9an4e2q94Wk5xd", "something", "something")
        self.swgoh_client = SwgohHelperClient(__credentials)

    def get_player_roster(self, player_ally_code):
        """
        Given a player's ally code, fetches its units.
        :param player_ally_code: Ally code of the player wanted
        :return: Json representation of the player's roster
        """

        request_payload = {
            "allycode": player_ally_code,
            "roster": True,
            "language": "ENG_US",
            # "stats": True,
            # "enums": True
            # "units": True,
            # "zetas": True
        }

        return self.swgoh_client.get_data("player", request_payload)

    def get_guild_units(self, guild_member_ally_code):
        """
        Given a player's ally code, fetches its guild's units.
        All units of all members of the guild will be fetched.
        :param guild_member_ally_code: A random member of the guild
        :return: Json representation of the guild's roster
        """

        request_json = {"allycode": guild_member_ally_code,
                        "roster": True,
                        "units": True,
                        "zetas": True,
                        "enums": True}

        return self.swgoh_client.get_data("guild", request_json)

    def get_game_units(self):
        """
        Get all units available in the game.
        :return: Json representation
        """

        request_payload = {"collection": "unitsList",
                           "language": "ENG_US",
                           "forceAlignment": True,
                           "enums": True}
        return self.swgoh_client.get_data("data", request_payload)

    def get_units_stats(self, units):
        """
        .......
        """
        print("YEPIA!!")
        request_payload = {"list": "rosterStats"}
        return self.swgoh_client.get_data("data", request_payload)

    def get_guild_players(self, guild_member_ally_code):
        """
        Get all players in guild.
        :return: Json representation
        """

        request_json = {"allycode": guild_member_ally_code}

        return self.swgoh_client.get_data("guild", request_json)

    def get_equipment_list(self):
        """
        .......
        """

        request_payload = {"collection": "playerPortraitList"}
        return self.swgoh_client.get_data("data", request_payload)
