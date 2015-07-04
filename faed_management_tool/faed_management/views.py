import forms, models
from django.views.generic import FormView, ListView
from rest_framework import viewsets
from serializers import HangarSerializer, DropPointSerializer,MeteoStationSerializer


#class PointListView(ListView):
#    context_object_name = 'points'
#    template_name = 'point_list.html'
#    queryset = models.Point.objects.all()


class HangarsView(ListView):
    template_name = 'hangars_list'
    context_object_name = 'hangar'
    queryset = models.Hangar.objects.all()

class DroneFormView(FormView):
    template_name = 'drone_form.html'
    form_class = forms.DroneForm
    success_url = "/droneform"

class StyleURLFormView(FormView):
    template_name = 'styleurl_form.html'
    form_class = forms.StyleURLForm
    success_url = "/styleurlform"

    def form_valid(self, form):
        if self.request.method == 'POST':
            return super(StyleURLFormView, self).form_valid(form)
        return None

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
