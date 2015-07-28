import os, forms, models, faed_management

from faed_management.static.py_func.sendtoLG import transfer, a
from kmls_management import kml_generator
from django.views.generic import FormView, ListView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from serializers import HangarSerializer, DropPointSerializer, MeteoStationSerializer
from faed_management.models import Hangar, DropPoint, MeteoStation, StyleURL, Drone
from faed_management.forms import HangarForm, MeteoStationForm, DropPointForm, StyleURLForm, DroneForm

#List items
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

class DropPointsList(ListView):
    model = DropPoint

class DropPointsView(ListView):
    template_name = 'droppoints.html'
    context_object_name = 'droppoints'
    queryset = models.DropPoint.objects.all()
    success_url = "/droppoints"


# Forms
def submit_styleurl(request):
    if request.method == 'POST':
        form = forms.StyleURLForm(request.POST)

        if form.is_valid():
            styleurl = form.save(commit=False)
            styleurl.save()

            return HttpResponseRedirect('/')
    else:
        form = forms.StyleURLForm()

    return render(request, 'styleurl_form.html', {'form': form})

def submit_droppoint(request):
    if request.method == 'POST':
        form = forms.DropPointForm(request.POST)

        if form.is_valid():
            droppoint = form.save(commit=False)
            droppoint.save()

            a()
            transfer()

            return HttpResponseRedirect('/droppoints/')
    else:
        form = forms.DropPointForm()

    return render(request, 'droppoint_form.html', {'form': form})

def submit_drone(request):
    if request.method == 'POST':
        form = forms.DroneForm(request.POST)

        if form.is_valid():
            drone = form.save(commit=False)
            drone.save()
            return HttpResponseRedirect('/hangars/')
        else:
            form = forms.DroneForm

    else:
        form = forms.DroneForm()

    return render(request, 'drone_form.html', {'form': form})

def submit_hangar(request):
    if request.method == 'POST':
        form = forms.HangarForm(request.POST)

        if form.is_valid():
            hangar = form.save(commit=False)
            hangar.drone.origin_lat = hangar.latitude
            hangar.drone.origin_lon = hangar.longitude
            #drone.altitude = altitude
            hangar.drone.save()
            hangar.save()

            a()
            transfer()

            return HttpResponseRedirect('/hangars/')
    else:
        form = forms.HangarForm()

    return render(request, 'hangar_form.html', {'form': form})

def submit_meteostation(request):
    if request.method == 'POST':
        form = forms.MeteoStationForm(request.POST)

        if form.is_valid():
            meteostation = form.save(commit=False)
            meteostation.save()

#            meteos = models.MeteoStation.objects.all()
#            for meteo in meteos:
#                kml_generator.placemark_kml(meteo,os.path.abspath(os.path.dirname(__file__)) + "/static/kml/meteo_" + str(meteo.id) + ".kml",
#                                            "http://www.latitude-voile.com/latitude_ecole_de_voile_la_baule/images/stories/PUB/acc_meteo.png",
#                                            "meteo_station")
            a()
            transfer()

            return HttpResponseRedirect('/meteostations/')
    else:
        form = forms.MeteoStationForm()

    return render(request, 'meteostation_form.html', {'form': form})


# REST API
class HangarViewSet(viewsets.ModelViewSet):
    queryset = models.Hangar.objects.all()
    serializer_class = HangarSerializer

class DropPointViewSet(viewsets.ModelViewSet):
    queryset = models.DropPoint.objects.all()
    serializer_class = DropPointSerializer

class MeteoStationViewSet(viewsets.ModelViewSet):
    queryset = models.MeteoStation.objects.all()
    serializer_class = MeteoStationSerializer


#Delte items
def delete_hangar(request, id):
    Hangar.objects.get(pk=id).delete()
    return HttpResponseRedirect('/hangars/')

def delete_droppoint(request, id):
    DropPoint.objects.get(pk=id).delete()
    return HttpResponseRedirect('/droppoints/')

def delete_meteostation(request, id):
    MeteoStation.objects.get(pk=id).delete()
    return HttpResponseRedirect('/meteostations/')


#Edit items
def edit_styleurl(request, id):
    requested_styleurl = StyleURL.objects.get(pk=id)
    form = StyleURLForm(instance=requested_styleurl)
    if request.method =='POST':
        form = StyleURLForm(request.POST, instance=requested_styleurl)
        if form.is_valid():
            styleurl = form.save(commit=False)
            styleurl.save()

            return HttpResponseRedirect('/')

    return render(request, 'styleurl_form.html', {'form': form})

def edit_drone(request, id):
    requested_drone = Drone.objects.get(pk=id)
    form = DroneForm(instance=requested_drone)
    if request.method =='POST':
        form = DroneForm(request.POST, instance=requested_drone)
        if form.is_valid():
            drone = form.save(commit=False)
            drone.save()

            return HttpResponseRedirect('/hangars')

    return render(request, 'drone_form.html', {'form': form})

def edit_hangar(request, id):
    requested_hangar = Hangar.objects.get(pk=id)
    form = HangarForm(instance=requested_hangar)
    if request.method =='POST':
        form = HangarForm(request.POST, instance=requested_hangar)
        if form.is_valid():
            hangar = form.save(commit=False)
            hangar.drone.origin_lat = hangar.latitude
            hangar.drone.origin_lon = hangar.longitude
            #drone.altitude = altitude
            hangar.drone.save()

            hangar.save()
            return HttpResponseRedirect('/hangars')
    return render(request, 'hangar_form.html',{'form':form})

def edit_meteostation(request, id):
    requested_meteo = MeteoStation.objects.get(pk=id)
    form = MeteoStationForm(instance=requested_meteo)
    if request.method == 'POST':
        form = HangarForm(request.POST, instance=requested_meteo)
        if form.is_valid():
            meteo_station = form.save(commit=False)
            meteo_station.save()

            return HttpResponseRedirect('/meteostations')

    return render(request, 'meteostation_form.html', {'form': form})

def edit_droppoint(request, id):
    requested_droppoint = DropPoint.objects.get(pk=id)
    form = DropPointForm(instance=requested_droppoint)
    if request.method == 'POST':
        form = DropPointForm(request.POST, instance=requested_droppoint)
        if form.is_valid():
            droppoint = form.save(commit=False)
            droppoint.save()
            return HttpResponseRedirect('/droppoints')

    return render(request, 'droppoint_form.html', {'form': form})