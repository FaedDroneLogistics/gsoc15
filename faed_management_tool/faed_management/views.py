from django.template.context_processors import request
import forms, models
from django.views.generic import FormView, ListView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from serializers import HangarSerializer, DropPointSerializer,MeteoStationSerializer
from faed_management.models import Hangar, DropPoint, MeteoStation

class HangarsList(ListView):
        model = Hangar

class HangarsView(ListView):
    template_name = 'hangars.html'
    context_object_name = 'hangars'
    queryset = models.Hangar.objects.all()
    success_url = "/hangars"


class MeteoStationsList(ListView):
    model = MeteoStation


class MeteoStationsView(ListView):
    template_name = 'meteostations.html'
    context_object_name = 'meteostations'
    queryset = models.MeteoStation.objects.all()
    success_url = "/meteostations"

class DropPointsView(ListView):
    template_name = 'droppoints.html'
    context_object_name = 'droppoints'
    queryset = models.DropPoint.objects.all()
    success_url = "/droppoints"

class DropPointsList(ListView):
        model = DropPoint

class DroneFormView(FormView):
    template_name = 'drone_form.html'
    form_class = forms.DroneForm
    success_url = "/droneform"

class DropPointFormView(FormView):
    template_name = 'droppoint_form.html'
    form_class = forms.DropPointForm
    success_url = "/droppointform"

class HangarFormView(FormView):
    template_name = 'hangar_form.html'
    form_class = forms.HangarForm
    success_url = "/hangarform"

class MeteoStationFormView(FormView):
    template_name = 'meteostation_form.html'
    form_class = forms.MeteoStationForm
    success_url = '/meteostationform'

#FORMS
def submit_styleurl(request):
    if request.method == 'POST':
        form = forms.StyleURLForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            href = form.cleaned_data['href']
            scale = form.cleaned_data['scale']

            style = models.StyleURL(name=name,href=href,scale=scale)
            style.save()

            return HttpResponseRedirect('/styleurlform/')
    else:
        form = forms.StyleURLForm()

    return render(request, 'styleurl_form.html', {'form': form})

def submit_droppoint(request):
    if request.method == 'POST':
        form = forms.DropPointForm(request.POST)

        if form.is_valid():

            return HttpResponseRedirect('/styleurlform/')


#REST API
class HangarViewSet(viewsets.ModelViewSet):
    queryset = models.Hangar.objects.all()
    serializer_class = HangarSerializer

class DropPointViewSet(viewsets.ModelViewSet):
    queryset = models.DropPoint.objects.all()
    serializer_class = DropPointSerializer

class MeteoStationViewSet(viewsets.ModelViewSet):
    queryset = models.MeteoStation.objects.all()
    serializer_class = MeteoStationSerializer


#def get_kml(request):
#    if request.GET.get('data_model') == 'hangar':
#        hangars = models.Hangar.objects.all()
