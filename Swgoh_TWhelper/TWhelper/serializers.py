
from rest_framework import serializers
from .models import ZetasNames, Rooster, Team


class ZetasSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ZetasNames
        fields = (
            'id', 'name'
        )
        read_only_fields = (
            'id', 'name'
        )


class RoosterSerializer(serializers.ModelSerializer):
    zeta_abs = ZetasSerializer()
    rooster = serializers.IntegerField(read_only=True)

    class Meta:
        model = Rooster
        fields = (
            'pk',
            'name', 'gp', 'gear_level', 'speed', 'star_level', 'num_zetas',
            'level', 'zeta_abs', 'date_updated', 'player', 'rooster'
        )
        read_only_fields = (
            'pk',
            'name', 'gp', 'gear_level', 'speed', 'star_level', 'num_zetas',
            'level', 'zeta_abs', 'date_updated', 'player', 'rooster'
        )


class TeamSerializer(serializers.ModelSerializer):
    toon1 = RoosterSerializer(read_only=True)
    toon2 = RoosterSerializer(read_only=True)
    toon3 = RoosterSerializer(read_only=True)
    toon4 = RoosterSerializer(read_only=True)
    toon5 = RoosterSerializer(read_only=True)

    class Meta:
        model = Team
        fields = (
            'pk', 'toon1', 'toon2', 'toon3', 'toon4', 'toon5', 'date_posted',
            'author', 'author_username', 'Totalgp', 'assignment'
        )
        read_only_fields = (
            'pk', 'toon1', 'toon2', 'toon3', 'toon4', 'toon5', 'date_posted',
            'author', 'author_username', 'Totalgp'
        )
