from django.contrib import admin
from .models import Team, Rooster, ZetasNames
from users.models import Profile

admin.site.register(Team)
admin.site.register(Rooster)
admin.site.register(ZetasNames)
admin.site.register(Profile)
