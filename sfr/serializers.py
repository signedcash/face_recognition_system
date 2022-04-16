from rest_framework import serializers

from sfr.models import FaceRec


class FaceRecSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceRec
        fields = ('img', 'code', 'device')
