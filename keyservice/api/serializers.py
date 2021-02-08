from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Position, MapPosition


class UserSigninSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ["id", "date", "url", "key", "city", "verified", "position"]


class MapPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapPosition
        fields = ["id", "date", "name", "key", "city", "verified", "position"]

