from swgohlib.experience_api_client import ExperienceAPIClient
from googleapi.google_sheets_client import GoogleSheetsAPI
from googleapi.google_sheets_client import SPREADSHEET_ID
from parsers.json_parser import JsonParser
import json
from utils.io_utils import get_file_path
import csv


def main():

    # update_guild_roster()
    # update_game_units_list()

    rows = get_rows_to_write("guild_roster.csv")

    google_api_client = GoogleSheetsAPI(SPREADSHEET_ID)
    google_api_client.write_data_to_range("Roster!B2", rows)


def update_guild_roster():
    client = ExperienceAPIClient()

    fifty_stars_darker_ally_code = "731131193"
    guild_roster = client.get_guild_units(fifty_stars_darker_ally_code)

    guild_roster_filename = "guild_roster.json"
    guild_roster_file_path = get_file_path(guild_roster_filename, "json")

    with open(guild_roster_file_path, "w") as output:
        json.dump(guild_roster, output)

    JsonParser.parse_guild_roster_to_csv(guild_roster_filename, "guild_roster.csv")


def update_game_units_list():
    client = ExperienceAPIClient()
    game_units = client.get_game_units()

    game_units_file_path = get_file_path("game_units_list.json", "json")

    with open(game_units_file_path, "w") as output:
        json.dump(game_units, output)


def get_rows_to_write(csv_file):
    csv_file_path = get_file_path(csv_file, "csv")

    rows = []

    with open(csv_file_path) as csvDataFile:
        csv_reader = csv.reader(csvDataFile)
        for row in csv_reader:
            rows.append(row)

    return rows


main()
