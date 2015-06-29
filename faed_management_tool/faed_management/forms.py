from django import forms

import models

class StyleURLForm(forms.Form):
    href = forms.URLField()
    scale = forms.FloatField()


class DropPointForm(forms.Form):
    name = forms.TextInput()
    description = forms.Textarea()
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    altitude = forms.FloatField()
    is_available = forms.BooleanField()
    style_url = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(DropPointForm, self).__init__(*args, **kwargs)
        self.fields['style_url'].choices = [(style.id, style.href) for style in models.StyleURL.objects.all()]

class DroneForm(forms.Form):
    plate = forms.TextInput()

class HangarForm(forms.Form):
    name = forms.TextInput()
    description = forms.Textarea()
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    altitude = forms.FloatField()
    radius = forms.FloatField()
    is_available = forms.BooleanField()
    style_url = forms.ChoiceField()
    drone = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(HangarForm, self).__init__(*args, **kwargs)
        self.fields['drone'].choices = [(drone.id, drone.plate) for drone in models.Drone.objects.all()]

class MeteoStationForm(forms.Form):
    name = forms.TextInput()
    description = forms.Textarea()
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    altitude = forms.FloatField()
    is_available = forms.BooleanField()
    temperature = forms.FloatField()
    wind_speed = forms.FloatField()
