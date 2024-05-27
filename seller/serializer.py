from rest_framework.serializers import ModelSerializer

from seller.models import Property, NearbyPlaces


class NearbyPlacesSerializer(ModelSerializer):
    class Meta:
        model = NearbyPlaces
        fields = '__all__'

class PropertySerializer(ModelSerializer):
    nearby = NearbyPlacesSerializer(read_only=True, many=True)
    class Meta:
        model = Property
        fields = '__all__'

