from django.shortcuts import render, redirect
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import numpy as np
from .models import Battlefield
from Battlefield.serializers import BattlefieldSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView, Response
from django.urls import reverse
# Create your views here.

test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)
response = openapi.Response('response description', "Hellp")


@swagger_auto_schema(
    method='POST',
    operation_summary='上傳策略說明',
    operation_description='N/A',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'Enemy': openapi.Schema(type=openapi.TYPE_ARRAY, title='敵方資訊',
                                    items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, title='ID',
                                                             description='戰艦編號'),
                                        'name': openapi.Schema(type=openapi.TYPE_STRING, title='Name',
                                                               description='戰艦型號'),
                                        'lat': openapi.Schema(type=openapi.TYPE_NUMBER, title='Latitude', max=90,
                                                              min=-90,
                                                              description='緯度'),
                                        'lng': openapi.Schema(type=openapi.TYPE_NUMBER, title='Longitude', max=180,
                                                              min=-180,
                                                              description='經度'),
                                        'threat': openapi.Schema(type=openapi.TYPE_NUMBER, title='Threat', max=1, min=0,
                                                                 description='威脅值'),
                                        'value': openapi.Schema(type=openapi.TYPE_NUMBER, title='Value', max=1, min=0,
                                                                description='價值'),
                                    })),
            'Ally': openapi.Schema(type=openapi.TYPE_ARRAY, title='我方資訊',
                                   items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                       'id': openapi.Schema(type=openapi.TYPE_INTEGER, title='ID',
                                                            description='戰艦編號'),
                                       'name': openapi.Schema(type=openapi.TYPE_STRING, title='Name',
                                                              description='戰艦型號'),
                                       'lat': openapi.Schema(type=openapi.TYPE_NUMBER, title='Latitude', max=90,
                                                             min=-90,
                                                             description='緯度'),
                                       'lng': openapi.Schema(type=openapi.TYPE_NUMBER, title='Longitude', max=180,
                                                             min=-180,
                                                             description='經度'),
                                       'Weapon': openapi.Schema(type=openapi.TYPE_ARRAY, title='武器資訊',
                                                                items=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                                                     properties={
                                                                                         'id': openapi.Schema(
                                                                                             type=openapi.TYPE_INTEGER,
                                                                                             title='ID',
                                                                                             description='飛彈編號'),
                                                                                         'type': openapi.Schema(
                                                                                             type=openapi.TYPE_STRING,
                                                                                             title='Name',
                                                                                             description='飛彈型號'),
                                                                                         'damage': openapi.Schema(
                                                                                             type=openapi.TYPE_NUMBER,
                                                                                             title='Threat', max=1,
                                                                                             min=0,
                                                                                             description='火力值'),
                                                                                         'cost': openapi.Schema(
                                                                                             type=openapi.TYPE_NUMBER,
                                                                                             title='Value', max='INF',
                                                                                             min='-INF',
                                                                                             description='成本'),
                                                                                         'num': openapi.Schema(
                                                                                             type=openapi.TYPE_INTEGER,
                                                                                             title='Num', max=4, min=0,
                                                                                             description='飛彈數量'),
                                                                                     })),
                                   })),
        }), responses={200: openapi.Schema(type='url', title='message',
                                                             description='POST 成功，回傳結果網址')})
@api_view(['POST'])
def testPOST(request):
    context = {}
    if request.method == 'POST':
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
            count = 0
            temp_val = value['missile'].copy()
            for wid, v in value['missile'].items():
                if v['num'] == 0:
                    temp_val.pop(wid, None)
                count += v['num']
            if count > 0:
                value['missile'] = temp_val
                value['ae_pair'] = key
                Policy.append(value)
        b = Battlefield(situation=data, policy=Policy)
        b.save()

    return Response({"message": reverse('get_result', kwargs={'bid':b.id})})


def get_result(request, bid):
    context = {}
    b = Battlefield.objects.filter(id=bid)
    if b:
        b = b[0]
        context = {'situation': json.dumps(b.situation), 'policy': json.dumps(b.policy)}
    return render(request, 'handleResult.html', context)


def get_map(request):
    context = {}
    return render(request, 'map.html', context)
