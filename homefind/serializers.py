from rest_framework import serializers
from .models import *

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class RealEstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstate
        fields = '__all__'
