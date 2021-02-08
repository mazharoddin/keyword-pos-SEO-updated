from rest_framework import serializers


class BarcodeSerializer(serializers.Serializer):
    img = serializers.ImageField()

