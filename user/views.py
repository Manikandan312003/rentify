from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from user.permissions import IsOwnerOrAdminOrReadOnlyPermission
from user.models import Profile
from seller.customPagePagination import CustomPagePagination
from user.serializer import ProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate


class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serial = ProfileSerializer(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        userObj = authenticate(**request.data)
        if userObj:
            token, created = Token.objects.get_or_create(user=userObj)
            return Response({"token": token.key})
        return Response(
            {"status": False, "error": "Invalid"}, status=status.HTTP_401_UNAUTHORIZED
        )


class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsOwnerOrAdminOrReadOnlyPermission]
    pagination_class = CustomPagePagination


class MyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ProfileSerializer(request.user.profile).data)
