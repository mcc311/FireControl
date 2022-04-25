from django.http import HttpResponseRedirect
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import numpy as np

def index(request):
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')


def redirect(request, z, x, y):
    return HttpResponseRedirect(f'http://[::]:8080/data/TaiwanEMap/#{z}/{x}/{y}')


@csrf_exempt
def testPOST(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        policy = {}
        for ally in data['Ally']:
            for target in data['Enemy']:
                policy[(ally['id'], target['id'])] = {'latlng': [ally['lat'], ally['lng']],
                                                     't_latlng': [target['lat'], target['lng']], 'missile': {}}

        for ally in data['Ally']:
            for target in data['Enemy']:
                for weapon in ally['Weapon']:
                    policy[(ally['id'], target['id'])]['missile'][weapon['id']] = {'type': weapon['type'], 'num': 0}
            for weapon in ally['Weapon']:
                for _ in range(int(weapon['num'])):
                    target = np.random.choice(data['Enemy'])
                    policy[(ally['id'], target['id'])]['missile'][weapon['id']]['num'] += 1


        Policy = []
        for key, value in policy.items():
            value['ae_pair'] = key
            Policy.append(value)
        print(Policy)
        context = {'GeoJSON': json.dumps(data), 'Policy': json.dumps(Policy)}
    except :
        context = {}
    return render(request, 'handleResult.html', context)
