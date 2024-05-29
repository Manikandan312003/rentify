from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from seller.models import Property, NearbyPlaces


class NearbyPlacesSerializer(ModelSerializer):
    class Meta:
        model = NearbyPlaces
        fields = "__all__"




class PropertySerializer(ModelSerializer):
    nearby = NearbyPlacesSerializer(required=False, many=True)

    class Meta:
        model = Property
        fields = "__all__"

    def validate(self, attrs):
        nearby_ids = self.initial_data.get('nearby', [])
        nearby = NearbyPlaces.objects.filter(id__in=nearby_ids)
        attrs['nearby'] = nearby
        return super().validate(attrs)

    def create(self, validated_data):
        nearbys = validated_data.pop('nearby', [])
        instance = super().create(validated_data=validated_data)
        for nearby in nearbys:
            instance.nearby.add(nearby)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        nearbys = validated_data.pop('nearby', [])
        instance = super().update(instance=instance, validated_data=validated_data)
        instance.nearby.clear()
        for nearby in nearbys:
            instance.nearby.add(nearby)
        instance.save()
        return instance
