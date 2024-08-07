from django.core.mail import send_mail
import os
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from seller.customPagePagination import CustomPagePagination
from seller.filters import PropertyFilter
from seller.serializer import *
from seller.models import *
import django_filters
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import BasePagination

from user.permissions import IsOwnerOrAdminOrReadOnlyPropertyPermission

class NoPagination(BasePagination):
    """
    A custom pagination class that does nothing, effectively disabling pagination.
    """
    def paginate_queryset(self, queryset, request, view=None):
        return None

    def get_paginated_response(self, data):
        return data

class NearByPlaceViewSet(ModelViewSet):
    serializer_class = NearbyPlacesSerializer
    queryset = NearbyPlaces.objects.all()
    pagination_class = NoPagination

import json
class PropertyViewSet(ModelViewSet):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrAdminOrReadOnlyPropertyPermission]
    pagination_class = CustomPagePagination
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_class = PropertyFilter

    def create(self, request, *args, **kwargs):
        data = request.data
        data["profile"] = request.user.profile.id
        data['nearby'] = request.data.getlist('nearby', [])
        s = PropertySerializer(data=data)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        data['nearby'] = request.data.getlist('nearby')
        s = PropertySerializer(instance=instance, data=data, partial=partial)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    

class Likes(APIView):
    def post(self, request):
        property = request.data["property"]
        try:
            Like.objects.create(property_id=property, profile=request.user.profile)
            return Response()
        except IntegrityError:
            return Response("Already liked in", status=status.HTTP_400_BAD_REQUEST)


EMAIL = os.getenv("EMAIL_ADDRESS")


def sendmailService(property: Property, profile: Profile):
    send_mail(
        "Buyer Interested", profile.getDetail(), EMAIL, [property.profile.user.email]
    )
    send_mail(
        "Seller Details", property.profile.getDetail(), EMAIL, [profile.user.email]
    )


class InterestedView(APIView):
    def post(self, request):
        property_id = request.data["property"]

        try:
            property = Property.objects.get(id=property_id)
            sendmailService(property, request.user.profile)
            Interested.objects.create(
                property_id=property_id, profile=request.user.profile
            )
            return Response()
        except IntegrityError:
            return Response(
                "Already interested in Please check mail for buyer detail",
                status=status.HTTP_400_BAD_REQUEST,
            )
