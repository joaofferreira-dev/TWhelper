
from django import forms
from .models import Rooster, Team, MandasAction
from django.contrib.auth.models import User
from django.urls import reverse
from django_select2 import forms as s2forms


class Toon_select(forms.ModelForm):

    class Meta:
        model = Rooster
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].queryset = Rooster.objects.none()


class Edit_Team(forms.ModelForm):

    class Meta:
        model = Team
        # Tuple!!
        fields = ['toon1', 'toon2', 'toon3', 'toon4', 'toon5']  # might be needed more stuff...
        widgets = {
            'toon1': s2forms.Select2Widget,
            'toon2': s2forms.Select2Widget,
            'toon3': s2forms.Select2Widget,
            'toon4': s2forms.Select2Widget,
            'toon5': s2forms.Select2Widget,
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        current_team = kwargs.pop('current_team', None)
        super(Edit_Team, self).__init__(*args, **kwargs)
        self.fields['toon1'].queryset = Rooster.objects.filter(
            player__username=user).order_by('-name').reverse()
        self.fields['toon2'].queryset = Rooster.objects.filter(
            player__username=user).order_by('-name').reverse()
        self.fields['toon3'].queryset = Rooster.objects.filter(
            player__username=user).order_by('-name').reverse()
        self.fields['toon4'].queryset = Rooster.objects.filter(
            player__username=user).order_by('-name').reverse()
        self.fields['toon5'].queryset = Rooster.objects.filter(
            player__username=user).order_by('-name').reverse()

        # Auto complete if editing team
        if current_team:
            self.fields['toon1'].initial = current_team.toon1_id
            self.fields['toon2'].initial = current_team.toon2_id
            self.fields['toon3'].initial = current_team.toon3_id
            self.fields['toon4'].initial = current_team.toon4_id
            self.fields['toon5'].initial = current_team.toon5_id

    def get_absolute_url(self):
        return reverse('TWhelper-teamsupdate', args=(self.pk,))


class Mandalorians_actions(forms.ModelForm):

    class Meta:
        model = MandasAction
        fields = ['btn']
