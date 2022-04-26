from django.http import HttpResponseRedirect
from django.shortcuts import render


def index(request):
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')


def redirect(request, z, x, y):
    return HttpResponseRedirect(f'http://[::]:8080/data/TaiwanEMap/#{z}/{x}/{y}')





def get_map(request):
    return render(request, 'map.html')
