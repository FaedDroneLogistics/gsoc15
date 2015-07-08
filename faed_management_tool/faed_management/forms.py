from django import forms

import models

class StyleURLForm(forms.Form):
    name = forms.CharField(label='name')
    href = forms.URLField(label='href', required=True)
    scale = forms.FloatField(label='scale')


class DropPointForm(forms.Form):
    name = forms.CharField(label='name')
    description = forms.CharField(widget=forms.Textarea,label='description')
    latitude = forms.FloatField(label='latitude')
    longitude = forms.FloatField(label='longitude')
    altitude = forms.FloatField(label='altitude')
    is_available = forms.BooleanField(label='is_available')
    style_url = forms.ChoiceField(label='style_url')

    def __init__(self, *args, **kwargs):
        super(DropPointForm, self).__init__(*args, **kwargs)
        self.fields['style_url'].choices = [(style.id, style.name) for style in models.StyleURL.objects.all()]

class DroneForm(forms.Form):
    name = forms.CharField(label='name')
    plate = forms.CharField(label='plate')
    style_url = forms.ChoiceField(label='style_url')

    def __init__(self, *args, **kwargs):
        super(DroneForm, self).__init__(*args, **kwargs)
        self.fields['style_url'].choices = [(style.id, style.name) for style in models.StyleURL.objects.all()]

class HangarForm(forms.Form):
    name = forms.CharField(label='name')
    description = forms.CharField(widget=forms.Textarea,label='description')
    latitude = forms.FloatField(label='latitude')
    longitude = forms.FloatField(label='longitude')
    altitude = forms.FloatField(label='altitude')
    radius = forms.FloatField(label='radius')
    is_available = forms.BooleanField(label='is_available')
    style_url = forms.ChoiceField(label='style_url')
    drone = forms.ChoiceField(label='drone')

    def __init__(self, *args, **kwargs):
        super(HangarForm, self).__init__(*args, **kwargs)
        self.fields['drone'].choices = [(drone.id, drone.name) for drone in models.Drone.objects.all()]
        self.fields['style_url'].choices = [(style.id, style.name) for style in models.StyleURL.objects.all()]

class MeteoStationForm(forms.Form):
    name = forms.CharField(label='name')
    description = forms.CharField(widget=forms.Textarea,label='description')
    latitude = forms.FloatField(label='latitude')
    longitude = forms.FloatField(label='longitude')
    altitude = forms.FloatField(label='altutude')
    is_available = forms.BooleanField(label='is_available')
    temperature = forms.FloatField(label='temperature')
    wind_speed = forms.FloatField(label='wind_speed')
    style_url = forms.ChoiceField(label='style_url')

    def __init__(self, *args, **kwargs):
        super(MeteoStationForm, self).__init__(*args, **kwargs)
        self.fields['style_url'].choices = [(style.id, style.name) for style in models.StyleURL.objects.all()]
