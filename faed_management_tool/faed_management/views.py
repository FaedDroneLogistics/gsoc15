import os, forms, models, faed_management

from faed_management.static.py_func.sendtoLG import transfer, a
from kmls_management import kml_generator
from django.views.generic import FormView, ListView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from serializers import HangarSerializer, DropPointSerializer, MeteoStationSerializer
from faed_management.models import Hangar, DropPoint, MeteoStation
from faed_management.forms import HangarForm, MeteoStationForm

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
            name = form.cleaned_data['name']
            href = form.cleaned_data['href']
            scale = form.cleaned_data['scale']

            style = models.StyleURL(name=name, href=href, scale=scale)
            style.save()

            return HttpResponseRedirect('/styleurlform/')
    else:
        form = forms.StyleURLForm()

    return render(request, 'styleurl_form.html', {'form': form})


def submit_droppoint(request):
    if request.method == 'POST':
        form = forms.DropPointForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            altitude = form.cleaned_data['altitude']
            is_available = form.cleaned_data['is_available']
            style_url = models.StyleURL.objects.get(id=form.cleaned_data['style_url'])

            droppoint = models.DropPoint(name=name, description=description, latitude=latitude, longitude=longitude,
                                         altitude=altitude, is_available=is_available, style_url=style_url)
            droppoint.save()

            return HttpResponseRedirect('/droppointform/')
    else:
        form = forms.DropPointForm()

    return render(request, 'droppoint_form.html', {'form': form})

def submit_drone(request):
    if request.method == 'POST':
        form = forms.DroneForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            plate = form.cleaned_data['plate']
            style_url = models.StyleURL.objects.get(id=form.cleaned_data['style_url'])

            drone = models.Drone(name=name, plate=plate, style_url=style_url)
            drone.save()

            return HttpResponseRedirect('/droneform/')
    else:
        form = forms.DroneForm()

    return render(request, 'drone_form.html', {'form': form})

def submit_hangar(request):
    if request.method == 'POST':
        form = forms.HangarForm(request.POST)

        if form.is_valid():
            print 'AHAHAHAHAHAHAHAHA'
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

def delete_hangar(request,id):
    Hangar.objects.get(pk=id).delete()
    return HttpResponseRedirect('/hangars/')

def delete_droppoint(request,id):
    DropPoint.objects.get(pk=id).delete()
    return HttpResponseRedirect('/droppoints/')

def delete_meteostation(request,id):
    MeteoStation.objects.get(pk=id).delete()
    return HttpResponseRedirect('/meteostations/')


def edit_hangar(request,id):
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

def edit_meteostation(request,id):
    requested_meteo = MeteoStation.objects.get(pk=id)
    form = MeteoStationForm(instance=requested_meteo)
    if request.method =='POST':
        form = HangarForm(request.POST, instance=requested_meteo)
        if form.is_valid():
            meteo_station = form.save(commit=False)
            meteo_station.save()

            return HttpResponseRedirect('/meteostations')
    return render(request, 'meteostation_form.html', {'form': form})
