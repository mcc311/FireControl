from django.http import HttpResponseRedirect
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def index(request):
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')


def redirect(request, z, x, y):
    return HttpResponseRedirect(f'http://[::]:8080/data/TaiwanEMap/#{z}/{x}/{y}')


@csrf_exempt
def testPOST(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        context = {'GeoJSON': json.dumps(data)}
    except :
        context = {}
    return render(request, 'handleResult.html', context)
