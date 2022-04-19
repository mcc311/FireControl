from rest_framework import serializers
from Vessel.models import Missile, Vessel


class MissileSerializer(serializers.ModelSerializer):
    many = True

    class Meta:
        model = Missile
        fields = '__all__'


class VesselSerializer(serializers.ModelSerializer):
    many = True

    class Meta:
        model = Vessel
        fields = '__all__'
