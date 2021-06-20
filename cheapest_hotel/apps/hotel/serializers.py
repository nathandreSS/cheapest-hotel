from rest_framework import serializers
from hotel.models import Hotel, Tax


class HotelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hotel
        fields = ['name', 'stars']


class TaxSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'