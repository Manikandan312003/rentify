from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from user.models import Profile
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password", "email"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def check(self, data):
        userObj = User.objects.get(username=data.get("username"))
        return User.check_password(userObj, data.get("password"))


class ProfileSerializer(ModelSerializer):
    user = UserSerializer(required=False, read_only=True)
    first_name = serializers.CharField(max_length=100, write_only=True)
    last_name = serializers.CharField(max_length=100, write_only=True)
    username = serializers.CharField(max_length=100, write_only=True)
    password = serializers.CharField(max_length=100, write_only=True)
    email = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = Profile
        fields = "__all__"

    def validate(self, attrs):
        first_name = attrs.get("first_name")
        last_name = attrs.get("last_name")
        username = attrs.get("username")
        password = attrs.get("password")
        email = attrs.get("email")
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "password": password,
            "email": email,
        }
        user_serializer = UserSerializer(data=data)
        self.user_serializer = user_serializer
        if user_serializer.is_valid():
            return attrs
        else:
            raise serializers.ValidationError(user_serializer.errors)

    def create(self, validated_data):
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        username = validated_data.pop("username")
        password = validated_data.pop("password")
        email = validated_data.pop("email")
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "password": password,
            "email": email,
        }
        user_serializer = UserSerializer(data=data)
        if user_serializer.is_valid():
            user = user_serializer.save()

            profile = Profile.objects.create(user=user, **validated_data)
            return profile
        else:
            raise serializers.ValidationError(user_serializer.errors)
