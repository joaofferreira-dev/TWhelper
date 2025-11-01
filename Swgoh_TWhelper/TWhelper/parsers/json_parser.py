
import json
import csv
from TWhelper.bot.utils.io_utils import get_file_path
from TWhelper.bot.swgohlib.guild_metrics import Guild
from TWhelper.models import Rooster, ZetasNames, Team
from django.utils import timezone
from django.contrib.auth.models import User
import progressbar


class JsonParser:

    @staticmethod
    def calculate_TotalGp(team, user):
        """
        Calculates total gp for a team

        :param character: Team info
        """

        toon1 = Rooster.objects.filter(name=team.toon1).filter(player_id=user)
        toon2 = Rooster.objects.filter(name=team.toon2).filter(player_id=user)
        toon3 = Rooster.objects.filter(name=team.toon3).filter(player_id=user)
        toon4 = Rooster.objects.filter(name=team.toon4).filter(player_id=user)
        toon5 = Rooster.objects.filter(name=team.toon5).filter(player_id=user)

        """
        HAVERÁ MELHOR MANEIRA??????????
        """
        for object in toon1:
            toon1_gp = object.gp
        for object in toon2:
            toon2_gp = object.gp
        for object in toon3:
            toon3_gp = object.gp
        for object in toon4:
            toon4_gp = object.gp
        for object in toon5:
            toon5_gp = object.gp

        totalGP = toon1_gp + toon2_gp + toon3_gp + toon4_gp + toon5_gp

        return(totalGP)

    @staticmethod
    def calculate_speed(character):
        """
        Calculates speed for a specific toon taking into account gear and mod
        boosts if aplicable

        :param character: Character info
        """
        speed = 0

        if "Speed" in character["stats"]["gear"]:
            speed += character["stats"]["gear"]["Speed"]
        if "Speed" in character["stats"]["mods"]:
            speed += character["stats"]["mods"]["Speed"]

        speed += character["stats"]["base"]["Speed"]
        return(speed)

    @staticmethod
    def get_zetas(character):
        """
        Gets zetas from json for a specific toon

        :param character: Character info
        """

        list_zetas = []

        for skills in character["skills"]:
            if skills["isZeta"] and skills["tier"] == skills["tiers"]:
                list_zetas.append(skills["nameKey"])

        return(list_zetas)

    @staticmethod
    def get_Objectlistzetas(character):
        """
        Gets zetas from database object for a specific toon

        :param character: Character object
        :returns: List of character object zetas
        """

        list_zetas_names = []

        queryset_toon = Rooster.objects.get(name=character.name,
                                            player_id=character.player_id)

        toon_abs = list(queryset_toon.zeta_abs.all())
        for zeta_name in toon_abs:
            list_zetas_names.append(zeta_name.name)

        return(list_zetas_names)

    @staticmethod
    def get_forceAlignment(character):
        """
        Gets force alignment(DARK/LIGHT) from json for a specific toon

        :param character: Character info
        """

        with open("TWhelper/json_repo/game_units.json", "r") as sourcefile:
            units_data = json.load(sourcefile)

        for unit in units_data:
            if character["nameKey"] == unit["nameKey"]:
                forceAlignment = unit["forceAlignment"]
                break

        return(forceAlignment)

    @staticmethod
    def parse_player_roster_to_db(json_data, player, ally_code):
        """
        Given a JSON File with the guild roster, parse it to a the site db.

        :param json_file: The json to parse
        """
        user = User.objects.filter(username=player).first()

        if not user:
            user = User.objects.filter(first_name=player).first()

        json_data = json_data[0]['roster']

        progBar = progressbar.ProgressBar()
        iterable = range(len(json_data))

        for iteration in progBar(iterable):

            character = json_data[iteration]
            # Filters out ships
            if character["combatType"] == 2:
                continue

            check_toon = Rooster.objects.filter(
                name=character["nameKey"]).filter(player_id=user)

            if character["relic"]["currentTier"] is "null":
                relic = 0
            else:
                relic = character["relic"]["currentTier"]

            # If toon is already present just modify stats
            if check_toon:
                for object in check_toon:

                    object.gp = character["gp"]
                    object.gear_level = character["gear"]
                    object.star_level = character["rarity"]
                    object.level = character["level"]
                    object.relic_level = relic - 2
                    # Must check the exitence of zetas
                    list_zetas = JsonParser.get_zetas(character)
                    # if len(list_zetas) != object.num_zetas:
                    if len(list_zetas) > 0:
                        db_zetasnames = JsonParser.get_Objectlistzetas(object)
                        for zeta_hab in list_zetas:

                            if zeta_hab in db_zetasnames:
                                continue

                            zeta = ZetasNames(name=zeta_hab)
                            zeta.save()
                            object.zeta_abs.add(zeta)
                            object.save()
                    # Existence of speed boosts in gear form and mods must
                    # must be accounted for
                    object.num_zetas = len(list_zetas)
                    object.speed = JsonParser.calculate_speed(character)
                    object.date_updated = timezone.now()
                    object.save()

                continue

            # Create Toon
            list_zetas = JsonParser.get_zetas(character)
            num_zetas = len(list_zetas)
            toon = Rooster(name=character["nameKey"],
                           gp=character["gp"],
                           relic_level=relic - 2,
                           gear_level=character["gear"],
                           num_zetas=num_zetas,
                           forceAlignment=JsonParser.get_forceAlignment(character),
                           speed=JsonParser.calculate_speed(character),
                           star_level=character["rarity"],
                           level=character["level"], player=user)

            toon.save()

            if num_zetas > 0:
                for zeta_hab in list_zetas:
                    zeta = ZetasNames(name=zeta_hab)
                    zeta.save()
                    toon.zeta_abs.add(zeta)
                    toon.save()

        # Now let's update team total power stats
        teams = Team.objects.filter(author=user)
        for team in teams:
            team.Totalgp = JsonParser.calculate_TotalGp(team, user)
            team.save()
