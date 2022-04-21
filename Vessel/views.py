from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response

from Vessel.models import Missile, Vessel
from Vessel.serializers import MissileSerializer, VesselSerializer

from rest_framework import viewsets
from django.http import HttpResponseRedirect


# Create your views here.
class ListViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)


class MissileViewSet(ListViewSet):
    queryset = Missile.objects.all()
    serializer_class = MissileSerializer


class VesselViewSet(ListViewSet):
    queryset = Vessel.objects.all()
    serializer_class = VesselSerializer


