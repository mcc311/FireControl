from django.shortcuts import render
from Vessel.models import Vessel, Missile
from django.views import generic
from django.shortcuts import redirect


class VesselListView(generic.ListView):
    model = Vessel
    context_object_name = 'vessel_list'
    queryset = Vessel.objects.all
    template_name = 'table.html'

class VesselUpdateView(generic.edit.UpdateView):
    model = Vessel
    fields = ['type_id', 'typename', 'belongs_to', 'value', 'fire1', 'fire2']
    template_name = 'vessel_update_form.html'

class MissileListView(generic.ListView):
    model = Missile
    context_object_name = 'missile_list'
    queryset = Missile.objects.all
    template_name = 'missile_table.html'

class MissileUpdateView(generic.edit.UpdateView):
    model = Missile
    fields = ['type', 'default_num', 'belongs_to', 'damage']
    template_name = 'missile_update_form.html'


def index(request):
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')

def profile(request):
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'profile.html')
def login(request):
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'login.html')
def table(request):
    # Render the HTML template index.html with the data in the context variable

    return render(request, 'table.html', {'Vessels': Vessel.objects.all})

def handler404(request, *args, **kwargs):
    response = render(request, '404.html')
    response.status_code = 404
    return response






def get_map(request):
    return render(request, 'map.html')
