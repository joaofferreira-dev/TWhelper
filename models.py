
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.urls import reverse
from django import forms
#from forms import Edit_Team as EdT_form

from multiselectfield import MultiSelectField
import arrow

"""
    PATCH to migrate so mysql
"""


class PatchedMultiSelectField(MultiSelectField):
    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)


class ZetasNames(models.Model):
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


# Class for toons in each individual player rooster
class Rooster(models.Model):
    name = models.CharField(max_length=30)
    gp = models.IntegerField(default='0')
    affiliation = models.CharField(max_length=12, default='None')
    relic_level = models.IntegerField(default='0')
    gear_level = models.IntegerField(default='0')
    num_zetas = models.IntegerField(default='0')
    speed = models.IntegerField(default='0')
    star_level = models.IntegerField(default='0')
    level = models.IntegerField(default='0')
    forceAlignment = models.CharField(max_length=10, default='None')
    zeta_abs = models.ManyToManyField(ZetasNames, related_name='zeta_ab')
    date_updated = models.DateTimeField(default=timezone.now)
    # deletes toon if user gets deleted
    player = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('player',)

    def toon_to_dict_json(self):
        return {
            "pk": self.pk,
            "name": self.name,
            "gp": self.gp,
            "gear_level": self.gear_level,
            "speed": self.speed,
            "star_level": self.star_level,
            "level": self.level,
            "zeta_abs": self.zeta_abs.zetas_to_json(),
            "date_updated": self. date_updated,
            "player": self.player.username
        }


# Class for teams to post
class Team(models.Model):
    toon1 = models.ForeignKey(Rooster, on_delete=models.CASCADE, related_name='toon1', default=None)
    toon2 = models.ForeignKey(Rooster, on_delete=models.CASCADE, related_name='toon2', default=None)
    toon3 = models.ForeignKey(Rooster, on_delete=models.CASCADE, related_name='toon3', default=None)
    toon4 = models.ForeignKey(Rooster, on_delete=models.CASCADE, related_name='toon4', default=None)
    toon5 = models.ForeignKey(Rooster, on_delete=models.CASCADE, related_name='toon5', default=None)
    date_posted = models.DateTimeField(default=arrow.utcnow().format('YYYY-MM-DD HH:mm'))
    # deletes team if user gets deleted
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_username = models.CharField(max_length=50, blank=True, default="")
    Totalgp = models.IntegerField(default='0')

    assignments = (('1', 'None'),
                   ('2', 'T1'),
                   ('3', 'T2'),
                   ('4', 'T3'),
                   ('5', 'T4'),
                   ('6', 'T6'),
                   ('7', 'T7'),
                   ('8', 'T9'),
                   ('9', 'T10'))
    assignment = PatchedMultiSelectField(choices=assignments, default=assignments[0][0])
    # assignment = models.CharField(max_length=20, default='None')

    # Treats toon1 as ("Leader")
    def __str__(self):
        return self.toon1.name

    def get_absolute_url(self):
        return reverse('TWhelper-editteams')

    class Meta:
        ordering = ('author',)

    def to_dict_json(self):
        return {
            "pk": self.pk,
            "toon1": self.toon1.toon_to_dict_json(),
            "toon2": self.toon2.toon_to_dict_json(),
            "toon3": self.toon3.toon_to_dict_json(),
            "toon4": self.toon4.toon_to_dict_json(),
            "toon5": self.toon5.toon_to_dict_json(),
            "date_posted": self.date_posted,
            "author": self.author.username
        }

    def save(self, *args, **kwargs):
        # If author_username is empty set it to the username.
        if not self.author_username:
            self.author_username = self.author.get_username()

        self.Totalgp = self.toon1.gp + self.toon2.gp + self.toon3.gp + self.toon4.gp + self.toon5.gp
        self.full_clean()
        # EdT_form.clean()

        # Now call the save() method on super to store the instance.
        super(Team, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        # If author_username is empty set it to the username.

        self.Totalgp = self.toon1.gp + self.toon2.gp + self.toon3.gp + self.toon4.gp + self.toon5.gp
        # self.full_clean()

        # Now call the save() method on super to store the instance.
        super(Team, self).save(*args, **kwargs)

    def clean(self):
        # Check if all elements in form are unique(NO repeating characters)

        form_list = [self.toon1, self.toon2, self.toon3, self.toon4, self.toon5]
        error_dict = {}

        flag = len(set(form_list)) == len(form_list)
        if not flag:
            error_dict['toon1'] = forms.ValidationError("Should be greater than f1")
        if error_dict:
            raise forms.ValidationError(error_dict)

        return error_dict


class MandasAction(models.Model):
    """
    This will handle the Mandalorians officer orders requests
    (!!! ESTA DESCRICAO PRECISA DE SER TRABALHADA !!!)
    """
    btn = models.CharField(max_length=10)

    def __str__(self):
        return self.btn
