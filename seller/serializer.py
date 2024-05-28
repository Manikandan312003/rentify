from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from seller.models import Property, NearbyPlaces


class NearbyPlacesSerializer(ModelSerializer):
    class Meta:
        model = NearbyPlaces
        fields = "__all__"


def getOrCreate(nearby):
    if type(nearby) is str:
        try:
            nearbyObj = NearbyPlaces.objects.get(id = nearby)
        except NearbyPlaces.DoesNotExist:
            raise serializers.ValidationError(f"Nearby with id{nearby} Does not exist")
    else:
        nearbySerial = NearbyPlacesSerializer(data=nearby)
        if nearbySerial.is_valid():
            nearbyObj = nearbySerial.save()
        else:
            raise serializers.ValidationError(nearbySerial.errors)
    return nearbyObj


class PropertySerializer(ModelSerializer):
    nearby = NearbyPlacesSerializer(required=False, many=True)

    class Meta:
        model = Property
        fields = "__all__"

    def to_internal_value(self, data):
        print(data)
        nearbyValues = data.pop("nearby", [])
        instance = super().to_internal_value(data)
        nearbyObjs = []
        for nearby in nearbyValues:
            nearbyObjs.append(getOrCreate(nearby=nearby))
        instance["nearby"] = nearbyObjs
        print(instance)
        return instance

    def create(self, validated_data):
        nearbys = validated_data.pop("nearby", [])
        property: Property = super().create(validated_data=validated_data)
        for nearby in nearbys:
            property.nearby.add(getOrCreate(nearby= nearby))
        print(property)
        return property

    def update(self, instance, validated_data):
        nearbys = validated_data.pop("nearby", [])
        instance = super().update(instance=instance, validated_data=validated_data)
        instance.nearby.clear()
        for nearby in nearbys:
            instance.nearby.add(nearby)
        return instance
