from django.http import HttpResponseRedirect
from django.shortcuts import render


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
    return render(request, 'table.html')

def handler404(request, *args, **kwargs):
    response = render(request, '404.html')
    response.status_code = 404
    return response
def redirect(request, z, x, y):
    return HttpResponseRedirect(f'http://[::]:8080/data/TaiwanEMap/#{z}/{x}/{y}')





def get_map(request):
    return render(request, 'map.html')
