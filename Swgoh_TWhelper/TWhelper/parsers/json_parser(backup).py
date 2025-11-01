import json
import csv
from TWhelper.bot.utils.io_utils import get_file_path
from TWhelper.bot.swgohlib.guild_metrics import Guild
from TWhelper.models import Rooster, ZetasNames
from django.utils import timezone
from django.contrib.auth.models import User


class JsonParser:

    @staticmethod
    def parse_guild_roster_to_db(json_file):
        """
        Given a JSON File with the guild roster, parse it to a the site db.

        :param json_file: The json to parse
        """
        roster_json_file_path = get_file_path(json_file, "json")

        with open(roster_json_file_path) as src_file:
            json_data = json.load(src_file)
            characters_names = JsonParser.__get_characters_dictionary()

            users = ['ZeSabre', 'dose']
            for player in users:
                print(player)
                user = User.objects.filter(username=player).first()

                for character in json_data["roster"]:
                    for attribute in json_data["roster"][character]:
                        if attribute["player"] == player:

                            check_toon = Rooster.objects.filter(
                                name=JsonParser.__get_char_name_from_dict(characters_names, character)).filter(player_id=user)
                            # If toon is already present just modify stats
                            if check_toon:
                                print("já existe")
                                for object in check_toon:

                                    object.gp = attribute["gp"]
                                    object.gear_level = attribute["gearLevel"]
                                    object.star_level = attribute["starLevel"]
                                    object.level = attribute["level"]
                                    object.num_zetas = len(attribute["zetas"])
                                    object.level = attribute["level"]
                                    # "zetas" check_toon.level = attribute["level"]
                                    object.speed = 0
                                    object.date_updated = timezone.now()
                                    object.save()
                                    print("Updated")

                                continue

                            # handle first zeta
                            num_zetas = len(attribute["zetas"])
                            if num_zetas > 0:
                                zeta = ZetasNames(name=attribute["zetas"][0])
                                zeta.save()

                                toon = Rooster(name=JsonParser.__get_char_name_from_dict(characters_names, character),
                                               gp=attribute["gp"], gear_level=attribute["gearLevel"],
                                               num_zetas=len(attribute["zetas"]), speed=0,
                                               star_level=attribute["starLevel"], level=attribute["level"], player=user, zeta_abs=zeta)

                            # handle other Zetas
                                toon.save()
                            else:
                                zeta = ZetasNames(None)
                                zeta.save()
                                toon = Rooster(name=JsonParser.__get_char_name_from_dict(characters_names, character),
                                               gp=attribute["gp"], gear_level=attribute["gearLevel"],
                                               num_zetas=len(attribute["zetas"]), speed=0,
                                               star_level=attribute["starLevel"], level=attribute["level"], player=user, zeta_abs=zeta)
                                # handle other Zetas
                                toon.save()

    @staticmethod
    def parse_guild_roster_to_csv(json_file, new_file_name):
        """
        Given a JSON File with the guild roster, parse it to a CSV file.

        :param json_file: The json to parse
        :param new_file_name: The name of the csv file to be writen
        """

        parsed_csv_file_path = get_file_path(new_file_name, "csv")
        roster_json_file_path = get_file_path(json_file, "json")

        with open(parsed_csv_file_path, "w", newline="") as output:
            with open(roster_json_file_path) as src_file:
                wr = csv.writer(output)
                json_data = json.load(src_file)

                writer = csv.DictWriter(
                    output,
                    fieldnames=["Player", "Character", "Type", "Stars",
                                "Level", "Gear", "GP", "# Zetas", "Zetas"]
                )
                writer.writeheader()

                characters_names = JsonParser.__get_characters_dictionary()

                for character in json_data["roster"]:
                    for attribute in json_data["roster"][character]:
                        row_array = [
                            attribute["player"],
                            JsonParser.__get_char_name_from_dict(characters_names, character),
                            str(attribute["type"]).capitalize(),
                            attribute["starLevel"],
                            attribute["level"],
                            attribute["gearLevel"],
                            attribute["gp"],
                            len(attribute["zetas"]),
                            attribute["zetas"]
                        ]
                        wr.writerow(row_array)

    @staticmethod
    def __get_characters_dictionary():
        game_units_json = get_file_path("game_units_list.json", "json")

        dictionary = {}

        with open(game_units_json) as src_file:
            json_data = json.load(src_file)

            for character in json_data:
                dictionary[character["baseId"]] = character["nameKey"]

        return dictionary

    @staticmethod
    def __get_char_name_from_dict(dictionary, char_base_id):
        if char_base_id in dictionary:
            return dictionary[char_base_id]
        else:
            return char_base_id

    @staticmethod
    def get_guild_metrics(file_path):
        result = Guild()

        with open(file_path) as src_file:
            json_data = json.load(src_file)

            result.guild_name = json_data["name"]
            result.n_members = json_data["members"]
            result.total_gp = json_data["gp"]

        return result
