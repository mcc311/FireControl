from rest_framework import serializers
from Battlefield.models import Battlefield


class BattlefieldSerializer(serializers.ModelSerializer):
    many = True

    class Meta:
        model = Battlefield
        fields = '__all__'


