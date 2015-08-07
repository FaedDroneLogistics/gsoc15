import os
import sys

from django.contrib.gis.measure import D
from django.contrib.gis.geos.point import Point
from django.views.generic import ListView
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework import viewsets

import forms
import models
from kmls_management.models import Kml
from faed_management.static.py_func.sendtoLG import syncKmlsToGalaxy, syncKmlsFile
from kmls_management import kml_generator
from serializers import HangarSerializer, DropPointSerializer, MeteoStationSerializer
from faed_management.models import Hangar, DropPoint, MeteoStation, StyleURL, Drone
from faed_management.forms import HangarForm, MeteoStationForm, DropPointForm, StyleURLForm, DroneForm

import simplekml
from polycircles import polycircles


# List items
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
            create_kml(droppoint, "droppoint", "create")
            syncKmlsFile()
            syncKmlsToGalaxy()

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
        form = forms.DroneForm()

        return render(request, 'drone_form.html', {'form': form})


def submit_hangar(request):
    if request.method == 'POST':
        form = forms.HangarForm(request.POST)

        if form.is_valid():
            hangar = form.save(commit=False)
            hangar.drone.origin_lat = hangar.latitude
            hangar.drone.origin_lon = hangar.longitude
            # drone.altitude = altitude
            hangar.drone.save()
            hangar.save()
            create_kml(hangar, "hangar", "create")
            syncKmlsFile()
            syncKmlsToGalaxy()

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
            create_kml(meteostation, "meteo", "create")
            syncKmlsFile()
            syncKmlsToGalaxy()
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


# Delte items
def delete_hangar(request, id):
    hangar = Hangar.objects.get(pk=id)
    delete_kml(hangar.id, "hangar")
    hangar.delete()
    return HttpResponseRedirect('/hangars/')


def delete_droppoint(request, id):
    droppoint = DropPoint.objects.get(pk=id)
    delete_kml(droppoint.id, "droppoint")
    droppoint.delete()
    return HttpResponseRedirect('/droppoints/')


def delete_meteostation(request, id):
    meteostation = MeteoStation.objects.get(pk=id)
    delete_kml(meteostation.id, "meteo")
    meteostation.delete()
    return HttpResponseRedirect('/meteostations/')


# Edit items
def edit_styleurl(request, id):
    requested_styleurl = StyleURL.objects.get(pk=id)
    form = StyleURLForm(instance=requested_styleurl)
    if request.method == 'POST':
        form = StyleURLForm(request.POST, instance=requested_styleurl)
        if form.is_valid():
            styleurl = form.save(commit=False)
            styleurl.save()

            return HttpResponseRedirect('/')

    return render(request, 'styleurl_form.html', {'form': form})


def edit_drone(request, id):
    requested_drone = Drone.objects.get(pk=id)
    form = DroneForm(instance=requested_drone)
    if request.method == 'POST':
        form = DroneForm(request.POST, instance=requested_drone)
        if form.is_valid():
            drone = form.save(commit=False)
            drone.save()

            return HttpResponseRedirect('/hangars')

    return render(request, 'drone_form.html', {'form': form})


def edit_hangar(request, id):
    requested_hangar = Hangar.objects.get(pk=id)
    form = HangarForm(instance=requested_hangar)
    if request.method == 'POST':
        form = HangarForm(request.POST, instance=requested_hangar)
        if form.is_valid():
            hangar = form.save(commit=False)
            hangar.drone.origin_lat = hangar.latitude
            hangar.drone.origin_lon = hangar.longitude
            # drone.altitude = altitude
            hangar.drone.save()
            hangar.save()
            create_kml(hangar, "hangar", "edit")

            syncKmlsFile()
            syncKmlsToGalaxy()

            return HttpResponseRedirect('/hangars')

    return render(request, 'hangar_form.html', {'form': form})


def edit_meteostation(request, id):
    requested_meteo = MeteoStation.objects.get(pk=id)
    form = MeteoStationForm(instance=requested_meteo)
    if request.method == 'POST':
        form = MeteoStationForm(request.POST, instance=requested_meteo)
        if form.is_valid():
            meteostation = form.save(commit=False)
            meteostation.save()
            create_kml(meteostation, "meteo", "edit")
            syncKmlsFile()
            syncKmlsToGalaxy()
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
            create_kml(droppoint, "droppoint", "edit")
            syncKmlsFile()
            syncKmlsToGalaxy()

            return HttpResponseRedirect('/droppoints')

    return render(request, 'droppoint_form.html', {'form': form})


# Support functions
def create_kml(item, type, action):
    name = type + "_" + str(item.id) + ".kml"
    path = os.path.dirname(__file__) + "/static/kml/" + name
    kml_generator.placemark_kml(item, path)

    if action == 'create':
        Kml(name=name, url="static/kml/" + name).save()

    if type == 'hangar':
        name_influence = hangar_influence(item)
        if action == 'create':
            Kml(name=name_influence, url="static/kml/" + name_influence).save()


def delete_kml(id, type):
    filename = type + "_" + str(id) + ".kml"
    path = os.path.dirname(__file__) + "/static/kml/"
    print filename
    for files in os.walk(path):
        print files
        if filename in files[2]:
            os.remove(path + filename)
            Kml.objects.get(name=filename).delete()
            if type == 'hangar':
                os.remove(path + "hangar_" + str(id) + "_inf.kml")
            return


def hangar_influence(hangar):
    name = "hangar_" + str(hangar.id) + "_inf.kml"
    path = os.path.dirname(__file__) + "/static/kml/" + name

    polycircle = polycircles.Polycircle(latitude=hangar.latitude,
                                        longitude=hangar.longitude,
                                        radius=hangar.radius*5,
                                        number_of_vertices=36)
    points_list = polycircle.to_lat_lon()
    latlonalt = []
    for tuple in points_list:
        tup = (tuple[1], tuple[0], hangar.altitude)
        latlonalt.append(tup)

    kml = simplekml.Kml(open=1)
    shape_polycircle = kml.newmultigeometry(name=hangar.name)
    pol = shape_polycircle.newpolygon()
    pol.outerboundaryis = latlonalt

    pol.altitudemode = simplekml.AltitudeMode.relativetoground
    pol.extrude = 5
    pol.style.polystyle.color = '00ff00ff'
    pol.style.linestyle.color = '0000ff00'

    '''
    pol = kml.newpolygon(name=hangar.description, outerboundaryis=polycircle.to_kml())
    pol.style.polystyle.color = simplekml.Color.changealphaint(200, simplekml.Color.darksalmon)
    '''
    kml.save(path)


    return name


# Geo functions
def find_emergency_path(request):
    lat = request.GET.get('lat', '')
    lon = request.GET.get('lng', '')

    print lat, lon

    last_distance = sys.maxint
    all_hangars = models.Hangar.objects.all()
    selected_hangar = None
    all_droppoints = models.DropPoint.objects.all()
    selected_droppoint = None
    point_location = Point(float(lon), float(lat))

    for droppoint in all_droppoints:
        distance = D(m=point_location.distance(Point(droppoint.longitude, droppoint.latitude)))
        print type(distance)
        if distance.m < last_distance:
            last_distance = distance.m
            selected_droppoint = droppoint

    last_distance = sys.maxint
    point_location = Point(selected_droppoint.longitude, selected_droppoint.latitude)
    for hangar in all_hangars:
        distance = D(m=point_location.distance(Point(hangar.longitude, hangar.latitude)))
        if distance.m < last_distance:
            last_distance = distance.m
            selected_hangar = hangar

    print selected_hangar.name, selected_droppoint.name

    return HttpResponse(selected_hangar)
