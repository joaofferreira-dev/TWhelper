import json
import csv
from bot.utils.io_utils import get_file_path
from bot.swgohlib.guild_metrics import Guild
from TWhelper.models import Rooster
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

            user = 'ZeSabre'

            for character in json_data["roster"]:
                for attribute in json_data["roster"][character]:
                    if attribute["player"] is user:
                        print("PING!")

                        user.rooster_set.create(name=JsonParser.__get_char_name_from_dict(characters_names, character),
                                                gp=attribute["gp"], gear_level=attribute["gearLevel"],
                                                num_zetas=len(attribute["zetas"]), speed=0,
                                                star_level=attribute["starLevel"], level=attribute["level"],
                                                zetas=attribute["zetas"])

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
