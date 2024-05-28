from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from seller.models import Property, NearbyPlaces


class NearbyPlacesSerializer(ModelSerializer):
    class Meta:
        model = NearbyPlaces
        fields = "__all__"




class PropertySerializer(ModelSerializer):
    nearby = NearbyPlacesSerializer(many=True)

    class Meta:
        model = Property
        fields = "__all__"

    def validate(self, attrs):
        print(attrs)
        nearbyids = self.initial_data.get('nearby', [])
        self.nearby = NearbyPlaces.objects.filter(id__in=nearbyids)
        print(self.nearby)
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('nearby', [])
        instance = super().create(validated_data= validated_data)
        instance.nearby = self.nearby

    def update(self, instance, validated_data):
        instance = super().update(instance=instance, validated_data=validated_data)
        instance.nearby.clear()
        for nearby in self.nearby:
            instance.nearby.add(nearby)
            print(instance.nearby)
        instance.save()
        return instance
